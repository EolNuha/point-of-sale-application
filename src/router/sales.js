/* eslint-disable no-unused-vars */
import SalesView from "../views/sales/SalesView.vue";
import DailySalesView from "../views/sales/DailySalesView.vue";
import NewSaleView from "../views/sales/NewSaleView.vue";
import SaleDetailsView from "../views/sales/SaleDetailsView.vue";

export default [
  {
    path: "/sales",
    name: "sales",
    component: SalesView,
    meta: {
      title: "sales",
      breadcrumb: [
        {
          text: (route) => "sales",
          to: "sales",
          active: true,
        },
      ],
    },
  },
  {
    path: "/sales/daily",
    name: "daily-sales",
    component: DailySalesView,
    meta: {
      title: "sales",
      breadcrumb: [
        {
          text: (route) => "sales",
          to: "sales",
          active: false,
        },
        {
          text: (route) => "dailySales",
          to: "daily-sales",
          active: true,
        },
      ],
    },
  },
  {
    path: "/sales/new-sale",
    name: "new-sale",
    component: NewSaleView,
    meta: {
      title: "newSale",
      breadcrumb: [
        {
          text: (route) => "sales",
          to: "sales",
          active: false,
        },
        {
          text: (route) => "newSale",
          to: "new-sale",
          active: true,
        },
      ],
    },
  },
  {
    path: "/sales/:saleId",
    name: "sale-view",
    component: SaleDetailsView,
    meta: {
      title: "saleDetails",
      breadcrumb: [
        {
          text: (route) => "sales",
          to: "sales",
          active: false,
        },
        {
          text: (route) => "dailySales",
          to: "daily-sales",
          active: false,
          query: true,
        },
        {
          text: (route) => `${route.meta.title}`,
          to: "sale-view",
          active: true,
        },
      ],
    },
  },
];
