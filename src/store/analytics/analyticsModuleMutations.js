export default {
  SET_SALES(state, payload) {
    state.sales = payload;
  },
  SET_PURCHASES(state, payload) {
    state.purchases = payload;
  },
  SET_PRODUCTS_SOLD_BY_AMOUNT(state, payload) {
    state.productsSoldbyAmount = payload;
  },
  SET_PRODUCT_STATS(state, payload) {
    state.productStats = payload;
  },
};
