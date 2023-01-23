export default {
  SET_SALES(state, data) {
    state.sales = data;
  },
  SET_SALES_GROSS_PROFIT(state, data) {
    state.salesGrossProfit = data;
  },
  SET_SALE_STATS(state, data) {
    state.sale = data;
  },
  SET_PURCHASES(state, data) {
    state.purchases = data;
  },
  SET_PURCHASE_STATS(state, data) {
    state.purchase = data;
  },
  SET_PRODUCTS_SOLD_BY_AMOUNT(state, data) {
    state.productsSoldbyAmount = data;
  },
  SET_PRODUCTS_SOLD_BY_GROSS_PROFIT(state, data) {
    state.productsSoldbyGrossProfit = data;
  },
  SET_PRODUCTS_SOLD_BY_NET_PROFIT(state, data) {
    state.productsSoldbyNetProfit = data;
  },
  SET_PRODUCT_STATS(state, data) {
    state.productStats = data;
  },
  SET_USERS_REVENUE(state, data) {
    state.usersRevenue = data;
  },
  SET_USER_STATS(state, data) {
    state.userStats = data;
  },
  SET_SELLER_STATS(state, data) {
    state.sellerStats = data;
  },
};
