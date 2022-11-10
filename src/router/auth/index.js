import decode from "jwt-decode";
import router from "@/router";
// import store from "@/store";
export function authRoutesGuard(router) {
  router.beforeEach(async (to, from, next) => {
    // store.dispatch("notificationsModule/getNotifications");
    if (to.meta.isPublic) {
      next();
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      next({
        path: "/signin",
        query: {
          redirectTo: to.fullPath,
        },
      });
      return;
    }

    const decodedAccessToken = decode(token);
    if (Date.now() >= decodedAccessToken.exp * 1000) {
      next({
        path: "/signin",
        query: {
          redirectTo: to.fullPath,
        },
      });
      return;
    }

    next();
  });
}

export async function logoutUser(redirectPath) {
  localStorage.removeItem("token");
  router.push({ name: redirectPath });
}
