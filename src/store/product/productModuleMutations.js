export default {
  SET_PRODUCTS(state, payload) {
    state.products = payload;
  },
  SET_PAGINATION(state, payload) {
    state.pagination = payload;
  },
  SET_PRODUCT(state, payload) {
    state.product = payload;
  },
};
