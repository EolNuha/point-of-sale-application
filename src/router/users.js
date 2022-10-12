/* eslint-disable no-unused-vars */
import UsersView from "../views/user/UsersView.vue";
import UserDetailsView from "../views/user/UserDetailsView.vue";
import CreateUserView from "../views/user/CreateUserView.vue";
export default [
  {
    path: "/users",
    name: "users",
    meta: {
      title: "Users",
      breadcrumb: [
        {
          text: (route) => "Users",
          to: "users",
          active: true,
        },
      ],
    },
    component: UsersView,
  },
  {
    path: "/users/new-user",
    name: "new-user",
    meta: {
      title: "New User",
      breadcrumb: [
        {
          text: (route) => "Users",
          to: "users",
          active: false,
        },
        {
          text: (route) => "New User",
          to: "new-user",
          active: true,
        },
      ],
    },
    component: CreateUserView,
  },
  {
    path: "/users/:userId",
    name: "user-details",
    meta: {
      title: "User Details",
      breadcrumb: [
        {
          text: (route) => "Users",
          to: "users",
          active: false,
        },
        {
          text: (route) => "User Details",
          to: "user-details",
          active: true,
        },
      ],
    },
    component: UserDetailsView,
  },
];
