export default {
  SET_SALES(state, payload) {
    state.sales = payload;
  },
  SET_SALE_STATS(state, payload) {
    state.sale = payload;
  },
  SET_PURCHASES(state, payload) {
    state.purchases = payload;
  },
  SET_PURCHASE_STATS(state, payload) {
    state.purchase = payload;
  },
  SET_PRODUCTS_SOLD_BY_AMOUNT(state, payload) {
    state.productsSoldbyAmount = payload;
  },
  SET_PRODUCT_STATS(state, payload) {
    state.productStats = payload;
  },
  SET_USERS_REVENUE(state, payload) {
    state.usersRevenue = payload;
  },
  SET_USER_STATS(state, payload) {
    state.userStats = payload;
  },
  SET_SELLER_STATS(state, payload) {
    state.sellerStats = payload;
  },
};
