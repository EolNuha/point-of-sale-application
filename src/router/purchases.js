/* eslint-disable no-unused-vars */
const PurchasesView = () => import("../views/purchases/PurchasesView.vue");
const DailyPurchasesView = () =>
  import("../views/purchases/DailyPurchasesView.vue");
const NewPurchaseView = () => import("../views/purchases/NewPurchaseView.vue");
const PurchaseDetailsView = () =>
  import("../views/purchases/PurchaseDetailsView.vue");

export default [
  {
    path: "/purchases",
    name: "purchases",
    component: PurchasesView,
    meta: {
      title: "purchases",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: true,
        },
      ],
    },
  },
  {
    path: "/purchases/daily",
    name: "daily-purchases",
    component: DailyPurchasesView,
    meta: {
      title: "purchases",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "dailyPurchases",
          to: "daily-purchases",
          active: true,
        },
      ],
    },
  },
  {
    path: "/purchases/new-purchase",
    name: "new-purchase",
    component: NewPurchaseView,
    meta: {
      title: "newPurchase",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "newPurchase",
          to: "new-purchase",
          active: true,
        },
      ],
    },
  },
  {
    path: "/purchases/daily/:purchaseId",
    name: "purchase-view",
    component: PurchaseDetailsView,
    props: { edit: false },
    meta: {
      title: "purchaseDetails",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "dailyPurchases",
          to: "daily-purchases",
          active: false,
          query: true,
        },
        {
          text: (route) => "purchaseDetails",
          to: "purchase-view",
          active: true,
        },
      ],
    },
  },
  {
    path: "/purchases/daily/edit/:purchaseId",
    name: "purchase-edit",
    component: PurchaseDetailsView,
    props: { edit: true },
    meta: {
      title: "editPurchase",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "dailyPurchases",
          to: "daily-purchases",
          active: false,
          query: true,
        },
        {
          text: (route) => "editPurchase",
          to: "purchase-edit",
          active: true,
        },
      ],
    },
  },
];
