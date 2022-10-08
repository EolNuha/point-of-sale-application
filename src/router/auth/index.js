import decode from "jwt-decode";
import router from "@/router";
export function authRoutesGuard(router) {
  router.beforeEach(async (to, from, next) => {
    if (to.meta.isPublic) {
      next();
      return;
    }

    const token = sessionStorage.getItem("token");
    if (!token) {
      next({
        path: "/signin",
        query: {
          redirectTo: `${window.location.pathname}${window.location.search}`,
        },
      });
      return;
    }

    const decodedAccessToken = decode(token);
    if (Date.now() >= decodedAccessToken.exp * 1000) {
      next({
        path: "/signin",
        query: {
          redirectTo: `${window.location.pathname}${window.location.search}`,
        },
      });
      return;
    }

    next();
  });
}

export async function logoutUser(redirectPath) {
  // Remove userData from localStorage
  // ? You just removed token from localStorage. If you like, you can also make API call to backend to blacklist used token
  sessionStorage.removeItem("token");
  router.push({ name: redirectPath });
}
