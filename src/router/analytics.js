/* eslint-disable no-unused-vars */
import ProductAnalytics from "../views/analytics/ProductsView.vue";
import SaleAnalytics from "../views/analytics/SalesView.vue";
import PurchaseAnalytics from "../views/analytics/PurchaseView.vue";
import UserAnalytics from "../views/analytics/UsersView.vue";
export default [
  {
    path: "/analytics/products",
    name: "product-analytics",
    component: ProductAnalytics,
    meta: {
      title: "productAnalytics",
      breadcrumb: [
        {
          text: (route) => "productAnalytics",
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
      title: "saleAnalytics",
      breadcrumb: [
        {
          text: (route) => "saleAnalytics",
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
      title: "purchaseAnalytics",
      breadcrumb: [
        {
          text: (route) => "purchaseAnalytics",
          to: "purchase-analytics",
          active: true,
        },
      ],
    },
  },
  {
    path: "/analytics/users",
    name: "user-analytics",
    component: UserAnalytics,
    meta: {
      title: "userAnalytics",
      breadcrumb: [
        {
          text: (route) => "userAnalytics",
          to: "user-analytics",
          active: true,
        },
      ],
    },
  },
];
