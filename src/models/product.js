class Product {
  constructor() {
    this.id = null;
    this.name = null;
    this.barcode = false;
    this.measure = "pcs";
    this.stock = null;
    this.tax = 0;
    this.purchasedPriceWOTax = null;
    this.purchasedPrice = null;
    this.sellingPrice = null;
    this.expirationDate = null;
    this.dateCreated = null;
    this.dateModified = null;
  }
  fromData(data) {
    this.id = data.id || null;
    this.name = data.name || null;
    this.barcode = data.barcode || false;
    this.measure = data.measure || "pcs";
    this.stock = data.stock || null;
    this.tax = data.tax || 0;
    this.purchasedPriceWOTax = data.purchasedPriceWOTax || null;
    this.purchasedPrice = data.purchasedPrice || null;
    this.sellingPrice = data.sellingPrice || null;
    this.expirationDate = data.expirationDate || null;
    this.dateCreated = data.dateCreated || null;
    this.dateModified = data.dateModified || null;
  }
}

export default Product;
