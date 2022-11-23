/* eslint-disable no-unused-vars */
const SalesView = () => import("../views/sales/SalesView.vue");
const DailySalesView = () => import("../views/sales/DailySalesView.vue");
const NewSaleView = () => import("../views/sales/NewSaleView.vue");
const SaleDetailsView = () => import("../views/sales/SaleDetailsView.vue");

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
    props: { edit: false },
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
  {
    path: "/sales/edit/:saleId",
    name: "sale-edit",
    component: SaleDetailsView,
    props: { edit: true },
    meta: {
      title: "editSale",
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
          to: "sale-edit",
          active: true,
        },
      ],
    },
  },
];
