export default {
  SET_SALES(state, data) {
    state.sales = data;
  },
  SET_PAGINATION(state, data) {
    state.pagination = data;
  },
  SET_SALE(state, data) {
    state.sale = data;
  },
  SET_CURRENT_SALES(state, data) {
    state.currentSales.find((x) => x.tab === data.tab).products = data.products;
  },
};
