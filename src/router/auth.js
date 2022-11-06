/* eslint-disable no-unused-vars */
import SigninView from "../views/user/SigninView.vue";
import SignupView from "../views/user/SignupView.vue";
export default [
  {
    path: "/signin",
    name: "signin",
    meta: {
      title: "signin",
      isPublic: true,
      hideNavbar: true,
    },
    component: SigninView,
  },
  {
    path: "/signup",
    name: "signup",
    meta: {
      title: "signup",
      isPublic: true,
      hideNavbar: true,
    },
    component: SignupView,
  },
];
