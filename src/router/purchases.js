/* eslint-disable no-unused-vars */
const PurchasesView = () => import("../views/purchases/PurchasesView.vue");
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
    path: "/purchases/:purchaseId",
    name: "purchase-view",
    component: PurchaseDetailsView,
    meta: {
      title: "purchaseDetails",
      breadcrumb: [
        {
          text: (route) => "purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "purchaseDetails",
          to: "purchase-view",
          active: true,
        },
      ],
    },
  },
];
