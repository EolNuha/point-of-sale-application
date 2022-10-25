export default {
  getPurchasesList: (state) => state.purchases.data,
  getPurchasesPagination: (state) => state.purchases.pagination,
  getPurchaseDetails: (state) => state.purchase,
  getSellersList: (state) => state.sellers.data,
  getSellersPagination: (state) => state.sellers.pagination,
};
