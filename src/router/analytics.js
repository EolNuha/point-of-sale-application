/* eslint-disable no-unused-vars */
import ProductAnalytics from "../views/analytics/ProductsView.vue";
import SaleAnalytics from "../views/analytics/SalesView.vue";
import PurchaseAnalytics from "../views/analytics/PurchaseView.vue";
export default [
  {
    path: "/analytics/products",
    name: "product-analytics",
    component: ProductAnalytics,
    meta: {
      title: "Product Analytics",
      breadcrumb: [
        {
          text: (route) => "Product Analytics",
          to: "product-analytics",
          active: true,
        },
      ],
    },
  },
  {
    path: "/analytics/sales",
    name: "sale-analytics",
    component: SaleAnalytics,
    meta: {
      title: "Sale Analytics",
      breadcrumb: [
        {
          text: (route) => "Sale Analytics",
          to: "sale-analytics",
          active: true,
        },
      ],
    },
  },
  {
    path: "/analytics/purchases",
    name: "purchase-analytics",
    component: PurchaseAnalytics,
    meta: {
      title: "Purchase Analytics",
      breadcrumb: [
        {
          text: (route) => "Purchase Analytics",
          to: "purchase-analytics",
          active: true,
        },
      ],
    },
  },
];
