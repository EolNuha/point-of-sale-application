export default {
  SET_PURCHASES(state, payload) {
    state.purchases = payload;
  },
  SET_PAGINATION(state, payload) {
    state.pagination = payload;
  },
  SET_PURCHASE(state, payload) {
    state.purchase = payload;
  },
  SET_SELLERS(state, payload) {
    state.sellers = payload;
  },
};
