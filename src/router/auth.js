/* eslint-disable no-unused-vars */
import SigninView from "../views/user/SigninView.vue";
import SignupView from "../views/user/SignupView.vue";
export default [
  {
    path: "/signin",
    name: "signin",
    meta: {
      title: "Sign In Page",
      isPublic: true,
      hideNavbar: true,
    },
    component: SigninView,
  },
  {
    path: "/signup",
    name: "signup",
    meta: {
      title: "Sign Up",
      isPublic: true,
      hideNavbar: true,
    },
    component: SignupView,
  },
];
