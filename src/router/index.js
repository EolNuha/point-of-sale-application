/* eslint-disable no-unused-vars */
import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import ProductsView from "../views/products/ProductsView.vue";
import CreateProductView from "../views/products/CreateProductView.vue";
import ProductDetailsView from "../views/products/ProductDetailsView.vue";
import SalesView from "../views/sales/SalesView.vue";
import DailySalesView from "../views/sales/DailySalesView.vue";
import NewSaleView from "../views/sales/NewSaleView.vue";
import SaleDetailsView from "../views/sales/SaleDetailsView.vue";
import PurchasesView from "../views/purchases/PurchasesView.vue";
import NewPurchaseView from "../views/purchases/NewPurchaseView.vue";
import PurchaseDetailsView from "../views/purchases/PurchaseDetailsView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    meta: {
      title: "Home Page",
    },
    component: HomeView,
  },
  {
    path: "/products",
    name: "products",
    component: ProductsView,
    meta: {
      title: "Products",
      breadcrumb: [
        {
          text: (route) => "Products",
          to: "products",
          active: true,
        },
      ],
    },
  },
  {
    path: "/products/create",
    name: "products-create",
    component: CreateProductView,
    meta: {
      title: "Create Product",
      breadcrumb: [
        {
          text: (route) => "Products",
          to: "products",
          active: false,
        },
        {
          text: (route) => "Create Product",
          to: "products-create",
          active: true,
        },
      ],
    },
  },
  {
    path: "/products/:productId",
    name: "product-view",
    component: ProductDetailsView,
    meta: {
      title: "Product Details",
      breadcrumb: [
        {
          text: (route) => "Products",
          to: "products",
          active: false,
        },
        {
          text: (route) => `${route.meta.title}`,
          to: "product-view",
          active: true,
        },
      ],
    },
  },
  {
    path: "/sales",
    name: "sales",
    component: SalesView,
    meta: {
      title: "Sales",
      breadcrumb: [
        {
          text: (route) => "Sales",
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
      title: "Sales",
      breadcrumb: [
        {
          text: (route) => "Sales",
          to: "sales",
          active: false,
        },
        {
          text: (route) => "Daily Sales",
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
      title: "New Sale",
      breadcrumb: [
        {
          text: (route) => "Sales",
          to: "sales",
          active: false,
        },
        {
          text: (route) => "New Sale",
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
      title: "Sale Details",
      breadcrumb: [
        {
          text: (route) => "Sales",
          to: "sales",
          active: false,
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

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes,
});

export default router;
