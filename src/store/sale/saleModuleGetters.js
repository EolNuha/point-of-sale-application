export default {
  getSalesList: (state) => state.sales,
  getSalesPagination: (state) => state.pagination,
  getSaleDetails: (state) => state.sale,
  getCurrentSaleProducts: (state) => (tab) => {
    return state.currentSales.find((x) => x.tab === tab)?.products;
  },
};
