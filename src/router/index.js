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
import OrdersView from "../views/orders/OrdersView.vue";
import NewOrderView from "../views/orders/NewOrderView.vue";
import OrderDetailsView from "../views/orders/OrderDetailsView.vue";
import PurchasesView from "../views/purchases/PurchasesView.vue";
import NewPurchaseView from "../views/purchases/NewPurchaseView.vue";

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
    path: "/orders",
    name: "orders",
    component: OrdersView,
    meta: {
      title: "Orders",
      breadcrumb: [
        {
          text: (route) => "Orders",
          to: "orders",
          active: true,
        },
      ],
    },
  },
  {
    path: "/orders/new-order",
    name: "new-order",
    component: NewOrderView,
    meta: {
      title: "New Order",
      breadcrumb: [
        {
          text: (route) => "Orders",
          to: "orders",
          active: false,
        },
        {
          text: (route) => "New Order",
          to: "new-order",
          active: true,
        },
      ],
    },
  },
  {
    path: "/orders/:orderId",
    name: "order-view",
    component: OrderDetailsView,
    meta: {
      title: "Order Details",
      breadcrumb: [
        {
          text: (route) => "Orders",
          to: "orders",
          active: false,
        },
        {
          text: (route) => `${route.meta.title}`,
          to: "order-view",
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
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes,
});

export default router;
