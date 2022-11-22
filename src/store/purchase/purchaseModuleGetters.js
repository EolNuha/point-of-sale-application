export default {
  getPurchasesList: (state) => state.purchases,
  getPurchasesPagination: (state) => state.pagination,
  getPurchaseDetails: (state) => state.purchase,
  getSellersList: (state) => state.sellers.data,
};
