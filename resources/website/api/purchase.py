from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from website.models.settings import Settings
from website.models.purchase import Purchase, PurchaseItem, PurchaseTax
from website.models.product import Product
from website.helpers import getPaginatedDict
from website.jsonify.purchase import (
    getTaxesList,
    getPurchasesList,
    getDailyPurchasesList,
    getDailyPurchaseDict,
    getSellersList,
    getSellerDict,
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
    purchase_create,
    sellers,
)
from website.helpers_functions.helpers_purchase import (
    add_product_to_purchase,
    get_expiration_date,
    calculate_totals,
    calculate_tax_and_price,
    purchase_excel_template,
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
parser.add_argument("file_name", type=str, default="purchases")
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
                add_product_to_purchase(product, purchase, current_time)
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
            "file_name": "",
            "type_filter[]": "",
        }
    )
    def get(self):
        args = parser.parse_args()
        search, sort_column, sort_dir, file_name = (
            args["search"],
            args["sort_column"],
            args["sort_dir"],
            args["file_name"],
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

        return purchase_excel_template(query_items, file_name)


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
        search, sort_column, sort_dir, file_name = (
            args["search"],
            args["sort_column"],
            args["sort_dir"],
            args["file_name"],
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

        query_items = (
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

        return purchase_excel_template(query_items, file_name)


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

    @purchase_rest.expect(purchase_create)
    def put(self, purchaseId):
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

        purchase = Purchase.query.filter_by(id=purchaseId).first_or_404()

        purchase.seller_name = seller["seller_name"]
        purchase.seller_invoice_number = seller["invoice_number"]
        purchase.seller_fiscal_number = seller["fiscal_number"]
        purchase.seller_tax_number = seller["tax_number"]
        purchase.purchase_type = seller["purchase_type"]
        purchase.user = current_user
        purchase.date_created = purchase_date
        purchase.date_modified = current_time

        db.session.flush()

        products_dict = {product["barcode"]: product for product in products}
        # product_barcodes = [int(product["barcode"]) for product in products]

        for item in purchase.purchase_items:
            if item.product_barcode in products_dict:
                # Call update function
                self.update_product_to_purchase(
                    purchase_item=item,
                    product=products_dict[item.product_barcode],
                    current_time=current_time,
                )
            else:
                # Call delete function
                self.delete_product_from_purchase(
                    barcode=item.product_barcode, purchase_item=item
                )

        purchase_items_barcodes = [
            purchase_item.product_barcode for purchase_item in purchase.purchase_items
        ]

        for product in products:
            if int(product["barcode"]) not in purchase_items_barcodes:
                # Call create function
                try:
                    add_product_to_purchase(product, purchase, current_time)
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
        return "Success", 200

    def update_product_to_purchase(self, purchase_item, product, current_time):
        found_product = Product.query.filter_by(
            barcode=purchase_item.product_barcode
        ).first()
        found_purchase_item = PurchaseItem.query.filter_by(id=purchase_item.id).first()
        found_purchase_tax = (
            PurchaseTax.query.filter_by(purchase_id=purchase_item.purchase_id)
            .filter_by(tax_value=purchase_item.tax_amount)
            .first()
        )

        (stock_difference) = self.calculate_stock(product, purchase_item)

        (
            tax_amount,
            product_purchased_price,
            product_purchased_price_wo_tax,
        ) = calculate_tax_and_price(product)

        (
            product_total_amount,
            total_tax_amount,
            total_wo_tax_value,
        ) = calculate_totals(tax_amount, product_purchased_price, product)

        expiration_date = get_expiration_date(product)
        measure = str(product["measure"])

        self.update_product(
            found_product,
            product,
            stock_difference,
            product_purchased_price_wo_tax,
            product_purchased_price,
            measure,
            expiration_date,
            current_time,
        )

        self.update_purchase_item(
            found_purchase_item,
            product,
            product_purchased_price_wo_tax,
            product_purchased_price,
            measure,
            expiration_date,
            product_total_amount,
            total_tax_amount,
            current_time,
        )

        tax_query = Settings.query.filter_by(settings_value=int(product["tax"])).one()
        self.update_purchase_tax(
            found_purchase_tax,
            tax_query,
            total_tax_amount,
            total_wo_tax_value,
            current_time,
        )

    def update_product(
        self,
        found_product,
        product,
        stock_difference,
        product_purchased_price_wo_tax,
        product_purchased_price,
        measure,
        expiration_date,
        current_time,
    ):
        found_product.stock += stock_difference
        found_product.tax = product["tax"]
        found_product.purchased_price_wo_tax = product_purchased_price_wo_tax
        found_product.purchased_price = product_purchased_price
        found_product.selling_price = product["selling_price"]
        found_product.measure = measure
        found_product.expiration_date = expiration_date
        found_product.date_modified = current_time

    def update_purchase_item(
        self,
        found_purchase_item,
        product,
        product_purchased_price_wo_tax,
        product_purchased_price,
        measure,
        expiration_date,
        product_total_amount,
        total_tax_amount,
        current_time,
    ):
        found_purchase_item.product_tax = product["tax"]
        found_purchase_item.product_purchased_price_wo_tax = (
            product_purchased_price_wo_tax
        )
        found_purchase_item.product_purchased_price = product_purchased_price
        found_purchase_item.product_selling_price = product["selling_price"]
        found_purchase_item.rabat = product["rabat"]
        found_purchase_item.product_measure = measure
        found_purchase_item.product_stock = Decimal(product["stock"]).quantize(
            FOURPLACES
        )
        found_purchase_item.total_amount = product_total_amount
        found_purchase_item.tax_amount = total_tax_amount
        found_purchase_item.product_expiration_date = expiration_date
        found_purchase_item.date_modified = current_time

    def update_purchase_tax(
        self,
        found_purchase_tax,
        tax_query,
        total_tax_amount,
        total_wo_tax_value,
        current_time,
    ):
        found_purchase_tax.tax_name = tax_query.settings_name
        found_purchase_tax.tax_alias = tax_query.settings_alias
        found_purchase_tax.tax_value = total_tax_amount
        found_purchase_tax.total_without_tax = total_wo_tax_value
        found_purchase_tax.date_modified = current_time

    def calculate_stock(self, product, purchase_item):
        purchase_item_stock = purchase_item.product_stock
        product_stock = Decimal(product["stock"]).quantize(FOURPLACES)
        stock_difference = product_stock - purchase_item_stock

        return stock_difference

    def delete_product_from_purchase(self, barcode, purchase_item):
        found_product = Product.query.filter_by(barcode=barcode).first()
        if found_product:
            found_product.stock -= Decimal(purchase_item.product_stock)

        PurchaseItem.query.filter_by(id=purchase_item.id).delete()
        PurchaseTax.query.filter_by(purchase_id=purchase_item.purchase_id).filter_by(
            tax_value=purchase_item.tax_amount
        ).delete()
        db.session.commit()
