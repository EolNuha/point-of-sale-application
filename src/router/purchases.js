/* eslint-disable no-unused-vars */
import PurchasesView from "../views/purchases/PurchasesView.vue";
import NewPurchaseView from "../views/purchases/NewPurchaseView.vue";
import PurchaseDetailsView from "../views/purchases/PurchaseDetailsView.vue";

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
