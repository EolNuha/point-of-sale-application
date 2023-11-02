import Product from "@/models/product";

export default {
  SET_PRODUCTS(state, data) {
    state.products = data;
  },
  SET_PAGINATION(state, data) {
    state.pagination = data;
  },
  SET_PRODUCT(state, data) {
    const product = new Product();
    product.fromData(data);
    state.product = product;
  },
};
