class Product {
  constructor() {
    this.id = null;
    this.name = null;
    this.barcode = false;
    this.measure = "pcs";
    this.stock = null;
    this.tax = 0;
    this.purchased_price_wo_tax = null;
    this.purchased_price = null;
    this.selling_price = null;
    this.expiration_date = null;
    this.date_created = null;
    this.date_modified = null;
  }
  fromData(data) {
    this.id = data.id || null;
    this.name = data.name || null;
    this.barcode = data.barcode || false;
    this.measure = data.measure || "pcs";
    this.stock = data.stock || null;
    this.tax = data.tax || 0;
    this.purchased_price_wo_tax = data.purchased_price_wo_tax || null;
    this.purchased_price = data.purchased_price || null;
    this.selling_price = data.selling_price || null;
    this.expiration_date = data.expiration_date?.substring(0, 10) || null;
    this.date_created = data.date_created || null;
    this.date_modified = data.date_modified || null;
  }
}

export default Product;
