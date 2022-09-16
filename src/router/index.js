import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import HomeView from "../views/HomeView.vue";
import CreateProductView from "../views/CreateProductView.vue";

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
    path: "/about",
    name: "about",
    meta: {
      title: "About Page",
    },
    component: () => import("@/views/AboutView.vue"),
  },
  {
    path: "/products/create",
    name: "products-create",
    meta: {
      title: "Create Product",
    },
    component: CreateProductView,
  },
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes,
});

export default router;
