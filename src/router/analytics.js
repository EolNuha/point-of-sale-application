/* eslint-disable no-unused-vars */
import ProductAnalytics from "../views/analytics/ProductsView.vue";
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
];
