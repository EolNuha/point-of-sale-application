from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from website.models.settings import Settings
from website.models.purchase import Purchase, PurchaseItem, PurchaseTax
from website.models.product import Product
from website.helpers import getPaginatedDict, sumListOfDicts
from website.jsonify.purchase import (
    getTaxesList,
    getPurchasesList,
    getDailyPurchasesList,
    getDailyPurchaseDict,
    getSellersList,
    getSellerDict,
    getDailyPurchasesListExcel,
    getPurchasesListExcel,
)
from website import db
from sqlalchemy import or_, asc, desc, func, and_
import decimal
from datetime import datetime, date, time
from website.token import currentUser
from flask_restx import Namespace, Resource, reqparse
from werkzeug.exceptions import BadRequest
from website.api_models.purchase import (
    grouped_purchases_data,
    detailed_purchases_data,
    sellers_data,
    detailed_purchases,
    purchase_edit,
    purchase_create,
    sellers,
)

purchase_rest = Namespace("Purchase")

parser = reqparse.RequestParser()
parser.add_argument("page", type=int, default=1)
parser.add_argument("per_page", type=int, default=20)
parser.add_argument("start_date", type=str, default="")
parser.add_argument("end_date", type=str, default="")
parser.add_argument("date", type=str, default="")
parser.add_argument("search", type=str, default="")
parser.add_argument("sort_column", type=str, default="date_created")
parser.add_argument("sort_dir", type=str, default="desc")
parser.add_argument(
    "type_filter[]",
    type=str,
    action="append",
    default=[
        "purchase",
        "investment",
        "expense",
    ],
)

Decimal = decimal.Decimal
FOURPLACES = Decimal(10) ** -4


@purchase_rest.route("purchases")
class CreatePurchase(Resource):
    @purchase_rest.expect(purchase_create)
    @purchase_rest.marshal_with(detailed_purchases)
    def post(self):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP
        current_user = currentUser(request)

        purchase_payload = purchase_rest.payload
        products = purchase_payload["products"]
        seller = purchase_payload["seller"]

        current_time = datetime.now()
        purchase_date_split = seller["purchase_date"].split("-")
        purchase_date = datetime.combine(
            date(
                year=int(purchase_date_split[0]),
                month=int(purchase_date_split[1]),
                day=int(purchase_date_split[2]),
            ),
            datetime.now().time(),
        )

        purchase = Purchase(
            total_amount=0,
            subtotal_amount=0,
            rabat_amount=0,
            seller_name=seller["seller_name"],
            seller_invoice_number=seller["invoice_number"],
            seller_fiscal_number=seller["fiscal_number"],
            seller_tax_number=seller["tax_number"],
            purchase_type=seller["purchase_type"],
            user=current_user,
            date_created=purchase_date,
            date_modified=current_time,
        )

        db.session.add(purchase)
        db.session.flush()

        for product in products:
            try:
                self.add_product_to_purchase(product, purchase, current_time)
            except IntegrityError as e:
                db.session.rollback()
                raise BadRequest("barcodeExistsDetailed")

        purchase.total_amount = (
            db.session.query(func.sum(PurchaseItem.total_amount))
            .filter_by(purchase_id=purchase.id)
            .scalar()
            or 0
        )
        purchase.subtotal_amount = (
            db.session.query(
                func.sum(PurchaseItem.total_amount - PurchaseItem.tax_amount)
            )
            .filter_by(purchase_id=purchase.id)
            .scalar()
            or 0
        )
        purchase.rabat_amount = (
            db.session.query(func.sum(PurchaseItem.rabat))
            .filter_by(purchase_id=purchase.id)
            .scalar()
            or 0
        )

        db.session.commit()

        return getDailyPurchaseDict(purchase)

    def add_product_to_purchase(self, product, purchase, current_time):
        product_stock = Decimal(product["stock"]).quantize(FOURPLACES)
        product_purchased_price_wo_tax = Decimal(product["purchased_price_wo_tax"])
        tax_percentage = Decimal(product["tax"]) / 100
        rabat_percentage = Decimal(product["rabat"]) / 100
        price_wo_rabat = product_purchased_price_wo_tax - (
            product_purchased_price_wo_tax * rabat_percentage
        )
        tax_amount = Decimal(price_wo_rabat * tax_percentage).quantize(FOURPLACES)
        product_purchased_price = Decimal(price_wo_rabat + tax_amount).quantize(
            FOURPLACES
        )
        product_total_amount = Decimal(
            product_purchased_price * product_stock
        ).quantize(FOURPLACES)

        total_tax_amount = Decimal(tax_amount * product_stock).quantize(FOURPLACES)

        expiration_date = self.get_expiration_date(product)

        product_query = Product.query.filter_by(name=product["product_name"]).first()
        measure = str(product["measure"])

        found_with_barcode = Product.query.filter_by(barcode=product["barcode"]).first()
        if found_with_barcode and found_with_barcode.name != product["product_name"]:
            if product_query and product_query.barcode != found_with_barcode.barcode:
                raise IntegrityError("barcodeExistsDetailed")

        if product_query:
            purchase_item = self.create_purchase_item(
                purchase,
                product_query,
                product,
                current_time,
                product_purchased_price,
                total_tax_amount,
                product_total_amount,
                measure,
                product_stock,
            )
            product_query.name = product["product_name"]
            product_query.barcode = product["barcode"]
            product_query.tax = product["tax"]
            product_query.purchased_price_wo_tax = product_purchased_price_wo_tax
            product_query.purchased_price = product_purchased_price
            product_query.selling_price = product["selling_price"]
            product_query.measure = measure
            product_query.stock += product_stock
            product_query.expiration_date = expiration_date
        elif found_with_barcode:
            purchase_item = self.create_purchase_item(
                purchase,
                found_with_barcode,
                product,
                current_time,
                product_purchased_price,
                total_tax_amount,
                product_total_amount,
                measure,
                product_stock,
            )
            found_with_barcode.name = product["product_name"]
            found_with_barcode.barcode = product["barcode"]
            found_with_barcode.tax = product["tax"]
            found_with_barcode.purchased_price_wo_tax = product_purchased_price_wo_tax
            found_with_barcode.purchased_price = product_purchased_price
            found_with_barcode.selling_price = product["selling_price"]
            found_with_barcode.measure = measure
            found_with_barcode.stock += product_stock
            found_with_barcode.expiration_date = expiration_date
        else:
            created_product = self.create_product(
                product, current_time, measure, expiration_date, product_stock
            )

            purchase_item = self.create_purchase_item(
                purchase,
                created_product,
                product,
                current_time,
                product_purchased_price,
                total_tax_amount,
                product_total_amount,
                measure,
                product_stock,
            )

        tax_query = self.get_or_create_tax_query(product["tax"])

        tax_value = Decimal(tax_amount * product_stock).quantize(FOURPLACES)
        total_wo_tax_value = product_total_amount - tax_value

        db.session.add(
            PurchaseTax(
                purchase=purchase,
                tax_name=tax_query.settings_name,
                tax_alias=tax_query.settings_alias,
                tax_value=tax_value,
                total_without_tax=total_wo_tax_value,
                date_created=current_time,
                date_modified=current_time,
            )
        )
        db.session.add(purchase_item)

    def get_expiration_date(self, product):
        if product["expiration_date"]:
            expiration_date = product["expiration_date"].split("-")
            expiration_date = datetime.combine(
                date(
                    year=int(expiration_date[0]),
                    month=int(expiration_date[1]),
                    day=int(expiration_date[2]),
                ),
                time.min,
            )
        else:
            expiration_date = None
        return expiration_date

    def create_purchase_item(
        self,
        purchase,
        product_query,
        product,
        current_time,
        product_purchased_price,
        tax_amount,
        product_total_amount,
        measure,
        product_stock,
    ):
        return PurchaseItem(
            purchase=purchase,
            product_id=product_query.id,
            product_barcode=product["barcode"],
            product_name=product["product_name"],
            product_tax=product["tax"],
            rabat=product["rabat"],
            product_purchased_price_wo_tax=product["purchased_price_wo_tax"],
            product_purchased_price=product_purchased_price,
            product_selling_price=product["selling_price"],
            product_stock=product_stock,
            product_measure=measure,
            tax_amount=tax_amount,
            total_amount=product_total_amount,
            date_created=current_time,
            date_modified=current_time,
        )

    def create_product(
        self, product, current_time, measure, expiration_date, product_stock
    ):
        product_purchased_price = Decimal(product["purchased_price_wo_tax"])
        created_product = Product(
            name=product["product_name"],
            barcode=product["barcode"],
            stock=product_stock,
            tax=product["tax"],
            purchased_price_wo_tax=product["purchased_price_wo_tax"],
            purchased_price=product_purchased_price,
            selling_price=product["selling_price"],
            measure=measure,
            expiration_date=expiration_date,
            date_created=current_time,
            date_modified=current_time,
        )

        db.session.add(created_product)
        return created_product

    def get_or_create_tax_query(self, tax_value):
        return Settings.query.filter_by(settings_value=int(tax_value)).one()


@purchase_rest.route("purchases/grouped")
class GetGroupedPurchases(Resource):
    @purchase_rest.doc(
        params={
            "page": "",
            "per_page": "",
            "start_date": "",
            "end_date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    @purchase_rest.marshal_with(grouped_purchases_data)
    def get(self):
        args = parser.parse_args()
        page, per_page, search, sort_column, sort_dir = (
            args["page"],
            args["per_page"],
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        custom_start_date = args["start_date"].split("-")
        custom_end_date = args["end_date"].split("-")

        date_start = datetime.combine(date(*map(int, custom_start_date)), time.min)
        date_end = datetime.combine(date(*map(int, custom_end_date)), time.max)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        purchase_query = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.seller_fiscal_number.ilike(looking_for),
                    Purchase.seller_tax_number.ilike(looking_for),
                )
            )
            .filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
        )

        purchase_query = purchase_query.filter(
            and_(Purchase.purchase_type.in_(type_filter))
        )

        paginated_items = (
            purchase_query.order_by(
                asc(sort_column) if sort_dir == "asc" else desc(sort_column)
            )
            .with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                Purchase.date_modified.label("date_modified"),
                func.sum(Purchase.rabat_amount).label("rabat_amount"),
                func.sum(Purchase.subtotal_amount).label("subtotal_amount"),
                func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(func.strftime("%Y-%m-%d", Purchase.date_created))
            .paginate(page=page, per_page=per_page)
        )

        items = getPurchasesList(paginated_items.items)

        for item in items:
            item_date = datetime.strptime(
                item["date_created"], "%d.%m.%Y, %H:%M:%S"
            ).date()

            taxes = (
                PurchaseTax.query.filter(
                    PurchaseTax.date_created <= datetime.combine(item_date, time.max),
                    PurchaseTax.date_created >= datetime.combine(item_date, time.min),
                )
                .order_by(PurchaseTax.tax_name.desc())
                .with_entities(
                    PurchaseTax.id.label("id"),
                    PurchaseTax.tax_name.label("tax_name"),
                    PurchaseTax.tax_alias.label("tax_alias"),
                    func.sum(PurchaseTax.tax_value).label("tax_value"),
                    func.sum(PurchaseTax.total_without_tax).label("total_without_tax"),
                )
                .group_by(PurchaseTax.tax_name)
                .all()
            )

            item["taxes"] = getTaxesList(taxes)

        return getPaginatedDict(items, paginated_items)


@purchase_rest.route("purchases/grouped/excel")
class GetGroupedPurchasesExcel(Resource):
    @purchase_rest.doc(
        params={
            "start_date": "",
            "end_date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    def get(self):
        args = parser.parse_args()
        search, sort_column, sort_dir = (
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        custom_start_date = args["start_date"].split("-")
        custom_end_date = args["end_date"].split("-")

        date_start = datetime.combine(date(*map(int, custom_start_date)), time.min)
        date_end = datetime.combine(date(*map(int, custom_end_date)), time.max)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        purchase_query = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.seller_fiscal_number.ilike(looking_for),
                    Purchase.seller_tax_number.ilike(looking_for),
                )
            )
            .filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
        )

        purchase_query = purchase_query.filter(
            and_(Purchase.purchase_type.in_(type_filter))
        )

        query_items = (
            purchase_query.order_by(
                asc(sort_column) if sort_dir == "asc" else desc(sort_column)
            )
            .with_entities(
                Purchase.id.label("id"),
                Purchase.date_created.label("date_created"),
                Purchase.date_modified.label("date_modified"),
                func.sum(Purchase.rabat_amount).label("rabat_amount"),
                func.sum(Purchase.subtotal_amount).label("subtotal_amount"),
                func.sum(Purchase.total_amount).label("total_amount"),
            )
            .group_by(func.strftime("%Y-%m-%d", Purchase.date_created))
            .all()
        )

        items = getPurchasesListExcel(query_items)

        for item in items:
            item_date = datetime.strptime(item["date"], "%d.%m.%Y").date()

            taxes = (
                PurchaseTax.query.filter(
                    PurchaseTax.date_created <= datetime.combine(item_date, time.max),
                    PurchaseTax.date_created >= datetime.combine(item_date, time.min),
                )
                .order_by(PurchaseTax.tax_name.desc())
                .with_entities(
                    PurchaseTax.id.label("id"),
                    PurchaseTax.tax_name.label("tax_name"),
                    PurchaseTax.tax_alias.label("tax_alias"),
                    func.sum(PurchaseTax.tax_value).label("tax_value"),
                    func.sum(PurchaseTax.total_without_tax).label("total_without_tax"),
                )
                .group_by(PurchaseTax.tax_name)
                .all()
            )

            for tax in taxes:
                item[f"{tax.tax_name}%"] = tax.tax_value

        return jsonify(items)


@purchase_rest.route("purchases/detailed")
class GetDetailedPurchases(Resource):
    @purchase_rest.doc(
        params={
            "page": "",
            "per_page": "",
            "start_date": "",
            "end_date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    @purchase_rest.marshal_with(detailed_purchases_data)
    def get(self):
        args = parser.parse_args()
        page, per_page, search, sort_column, sort_dir = (
            args["page"],
            args["per_page"],
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        custom_start_date = args["start_date"].split("-")
        custom_end_date = args["end_date"].split("-")

        date_start = datetime.combine(date(*map(int, custom_start_date)), time.min)
        date_end = datetime.combine(date(*map(int, custom_end_date)), time.max)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        paginated_items = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.seller_fiscal_number.ilike(looking_for),
                    Purchase.seller_tax_number.ilike(looking_for),
                )
            )
            .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))
            .filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
            .filter(and_(Purchase.purchase_type.in_(type_filter)))
            .paginate(page=page, per_page=per_page)
        )

        return getPaginatedDict(
            getDailyPurchasesList(paginated_items.items), paginated_items
        )


@purchase_rest.route("purchases/detailed/excel")
class GetDetailedPurchasesExcel(Resource):
    @purchase_rest.doc(
        params={
            "start_date": "",
            "end_date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    def get(self):
        args = parser.parse_args()
        search, sort_column, sort_dir = (
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        custom_start_date = args["start_date"].split("-")
        custom_end_date = args["end_date"].split("-")

        date_start = datetime.combine(date(*map(int, custom_start_date)), time.min)
        date_end = datetime.combine(date(*map(int, custom_end_date)), time.max)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        query_items = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.seller_fiscal_number.ilike(looking_for),
                    Purchase.seller_tax_number.ilike(looking_for),
                )
            )
            .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))
            .filter(Purchase.date_created <= date_end)
            .filter(Purchase.date_created >= date_start)
            .filter(and_(Purchase.purchase_type.in_(type_filter)))
            .all()
        )

        return jsonify(getDailyPurchasesListExcel(query_items))


@purchase_rest.route("purchases/daily/excel")
class GetDailyPurchasesExcel(Resource):
    @purchase_rest.doc(
        params={
            "date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    def get(self):
        args = parser.parse_args()
        search, sort_column, sort_dir = (
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        purchase_date = args["date"].split(".")
        purchase_date.reverse()

        purchase_date_start = datetime.combine(date(*map(int, purchase_date)), time.min)
        purchase_date_end = datetime.combine(date(*map(int, purchase_date)), time.max)

        if sort_column == "tax":
            sort_column = func.lower(PurchaseTax.tax_value)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        paginated_items = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.total_amount.ilike(looking_for),
                    Purchase.subtotal_amount.ilike(looking_for),
                )
            )
            .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))
            .filter(Purchase.date_created <= purchase_date_end)
            .filter(Purchase.date_created >= purchase_date_start)
            .filter(and_(Purchase.purchase_type.in_(type_filter)))
            .all()
        )

        return jsonify(getDailyPurchasesListExcel(paginated_items))


@purchase_rest.route("purchases/daily")
class GetDailyPurchases(Resource):
    @purchase_rest.doc(
        params={
            "page": "",
            "per_page": "",
            "date": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
            "type_filter[]": "",
        }
    )
    @purchase_rest.marshal_with(detailed_purchases_data)
    def get(self):
        args = parser.parse_args()
        page, per_page, search, sort_column, sort_dir = (
            args["page"],
            args["per_page"],
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )
        type_filter = args["type_filter[]"] or ["purchase", "investment", "expense"]

        purchase_date = args["date"].split(".")
        purchase_date.reverse()

        purchase_date_start = datetime.combine(date(*map(int, purchase_date)), time.min)
        purchase_date_end = datetime.combine(date(*map(int, purchase_date)), time.max)

        if sort_column == "tax":
            sort_column = func.lower(PurchaseTax.tax_value)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        paginated_items = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.total_amount.ilike(looking_for),
                    Purchase.subtotal_amount.ilike(looking_for),
                )
            )
            .order_by(asc(sort_column) if sort_dir == "asc" else desc(sort_column))
            .filter(Purchase.date_created <= purchase_date_end)
            .filter(Purchase.date_created >= purchase_date_start)
            .filter(and_(Purchase.purchase_type.in_(type_filter)))
            .paginate(page=page, per_page=per_page)
        )

        return getPaginatedDict(
            getDailyPurchasesList(paginated_items.items), paginated_items
        )


@purchase_rest.route("sellers")
class GetSellers(Resource):
    @purchase_rest.doc(
        params={
            "page": "",
            "per_page": "",
            "sort_column": "",
            "sort_dir": "",
            "search": "",
        }
    )
    @purchase_rest.marshal_with(sellers_data)
    def get(self):
        args = parser.parse_args()
        page, per_page, search, sort_column, sort_dir = (
            args["page"],
            args["per_page"],
            args["search"],
            args["sort_column"],
            args["sort_dir"],
        )

        sort = asc(sort_column) if sort_dir == "asc" else desc(sort_column)

        looking_for = (
            search.strip().replace("_", "__").replace("*", "%").replace("?", "_")
            if "*" in search or "_" in search
            else f"%{search.strip()}%"
        )

        paginated_items = (
            Purchase.query.filter(
                or_(
                    Purchase.id.ilike(looking_for),
                    Purchase.seller_name.ilike(looking_for),
                    Purchase.seller_invoice_number.ilike(looking_for),
                    Purchase.seller_fiscal_number.ilike(looking_for),
                    Purchase.seller_tax_number.ilike(looking_for),
                )
            )
            .order_by(sort)
            .with_entities(
                Purchase.id.label("id"),
                Purchase.seller_name.label("seller_name"),
                Purchase.seller_fiscal_number.label("seller_fiscal_number"),
                Purchase.seller_tax_number.label("seller_tax_number"),
                Purchase.seller_invoice_number.label("seller_invoice_number"),
                Purchase.date_created.label("date_created"),
                Purchase.date_modified.label("date_modified"),
            )
            .group_by(Purchase.seller_name)
            .paginate(page=page, per_page=per_page)
        )

        return getPaginatedDict(getSellersList(paginated_items.items), paginated_items)


@purchase_rest.route("sellers/<string:name>")
class SellerDetails(Resource):
    @purchase_rest.marshal_with(sellers)
    def get(self, name):
        return getSellerDict(Purchase.query.filter_by(seller_name=name).first_or_404())


@purchase_rest.route("purchases/<int:purchaseId>")
class PurchaseDetails(Resource):
    @purchase_rest.marshal_with(detailed_purchases)
    def get(self, purchaseId):
        return getDailyPurchaseDict(
            Purchase.query.filter_by(id=purchaseId).first_or_404()
        )

    def delete(self, purchaseId):
        purchase_query = Purchase.query.filter_by(id=purchaseId).first_or_404()

        for item in purchase_query.purchase_items:
            product = Product.query.filter_by(id=item.product_id).first()
            if not product:
                product = Product.query.filter_by(barcode=item.product_barcode).first()
            if product:
                product.stock -= Decimal(item.product_stock)

        PurchaseItem.query.filter_by(purchase_id=purchaseId).delete()
        PurchaseTax.query.filter_by(purchase_id=purchaseId).delete()
        Purchase.query.filter_by(id=purchaseId).delete()
        db.session.commit()
        return "Success", 200

    @purchase_rest.expect(purchase_edit)
    def put(self, purchaseId):
        ctx = decimal.getcontext()
        ctx.rounding = decimal.ROUND_HALF_UP

        deleted_items = purchase_rest.payload["deletedItems"]
        purchase_items = purchase_rest.payload["purchase_items"]

        purchase_query = Purchase.query.filter_by(id=purchaseId).first_or_404()
        subtotal, purchase_taxes = [], []
        taxes = Settings.query.filter_by(settings_type="tax").all()

        for item in deleted_items:
            product = Product.query.filter_by(
                barcode=item["product"]["barcode"]
            ).first()
            if product:
                product.stock -= Decimal(item["product"]["stock"])
            PurchaseItem.query.filter_by(id=item["id"]).delete()
            PurchaseTax.query.filter_by(purchase_id=purchaseId).filter_by(
                tax_name=item["product"]["tax"]
            ).delete()
            db.session.commit()

        for item in purchase_items:
            item_stock = Decimal(item["product"]["stock"]).quantize(FOURPLACES)
            item_purchased_price = Decimal(item["product"]["purchased_price"]).quantize(
                FOURPLACES
            )
            item_tax = Decimal(item["product"]["tax"]).quantize(FOURPLACES)
            tax_amount = Decimal(
                Decimal(item_tax / 100).quantize(FOURPLACES) * item_purchased_price
            ).quantize(FOURPLACES)
            item_purchased_price_wo_tax = item_purchased_price - tax_amount

            subtotal.append(
                Decimal(item_purchased_price_wo_tax * item_stock).quantize(FOURPLACES)
            )

            for tax in taxes:
                if item["product"]["tax"] == int(tax.settings_value):
                    key_v = tax.settings_name + "+" + tax.settings_alias
                    purchase_taxes.append({key_v: tax_amount * item_stock})

            purchase_item = PurchaseItem.query.filter_by(id=item["id"]).first()

            purchase_item.product_stock = item_stock
            purchase_item.product_purchased_price_wo_tax = item_purchased_price_wo_tax
            purchase_item.product_purchased_price = item_purchased_price
            purchase_item.tax_amount = tax_amount
            purchase_item.total_amount = Decimal(
                Decimal(item_purchased_price).quantize(FOURPLACES) * Decimal(item_stock)
            ).quantize(FOURPLACES)

            product = Product.query.filter_by(
                barcode=item["product"]["barcode"]
            ).first()
            if product:
                product.stock += item_stock - purchase_item.product_stock
                product.purchased_price_wo_tax = item_purchased_price_wo_tax
                product.purchased_price = item_purchased_price

            db.session.commit()

        purchase_query.subtotal_amount = sum(subtotal)
        purchase_taxes = sumListOfDicts(purchase_taxes)

        for key, value in purchase_taxes.items():
            split_key = key.split("+")
            purchase_tax = PurchaseTax.query.filter(
                PurchaseTax.purchase_id.like(purchaseId),
                PurchaseTax.tax_name.ilike(split_key[0]),
            ).first()
            purchase_tax.tax_value = value
            purchase_tax.date_modified = datetime.now()
            db.session.commit()

        total_sum = (
            PurchaseItem.query.filter_by(purchase_id=purchaseId)
            .with_entities(func.sum(PurchaseItem.total_amount).label("total"))
            .first()
            .total
        )
        purchase_query.total_amount = total_sum
        db.session.commit()
        return "Success", 200
