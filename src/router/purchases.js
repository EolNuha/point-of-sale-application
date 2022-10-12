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
      title: "Purchases",
      breadcrumb: [
        {
          text: (route) => "Purchases",
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
      title: "New Purchase",
      breadcrumb: [
        {
          text: (route) => "Purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "New Purchase",
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
      title: "Purchase Details",
      breadcrumb: [
        {
          text: (route) => "Purchases",
          to: "purchases",
          active: false,
        },
        {
          text: (route) => "Purchase Details",
          to: "purchase-view",
          active: true,
        },
      ],
    },
  },
];
