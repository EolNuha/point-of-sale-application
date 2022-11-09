/* eslint-disable no-unused-vars */
import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import { authRoutesGuard } from "./auth/index";
import auth from "./auth";
import dashboard from "./dashboard";
import errorPages from "./errorPages";
import products from "./products";
import sales from "./sales";
import purchases from "./purchases";
import users from "./users";
import analytics from "./analytics";
import notifications from "./notifications";
import settings from "./settings";
import development from "./development";

const routes = [
  ...auth,
  ...dashboard,
  ...errorPages,
  ...products,
  ...sales,
  ...purchases,
  ...users,
  ...analytics,
  ...notifications,
  ...settings,
  ...(process.env.NODE_ENV === "development" ? [...development] : []),
  { path: "/:catchAll(.*)", redirect: "/404" },
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
});

authRoutesGuard(router);

export default router;
