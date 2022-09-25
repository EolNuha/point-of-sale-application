/* eslint-disable no-unused-vars */
import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import CreateProductView from "../views/CreateProductView.vue";
import ProductDetailsView from "../views/ProductDetailsView.vue";
import ProductsView from "../views/ProductsView.vue";
import NewSaleView from "../views/NewSaleView.vue";

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
    component: NewSaleView,
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
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes,
});

export default router;
