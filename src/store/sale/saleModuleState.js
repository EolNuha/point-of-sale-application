import Pagination from "@/models/pagination";

export default {
  sales: [],
  pagination: new Pagination(),
  sale: {},
  currentSales: [{ tab: 0, products: [] }],
  currentTabs: [0],
  typeFilters: [],
};
