/* eslint-disable no-unused-vars */
import UsersView from "../views/user/UsersView.vue";
import UserDetailsView from "../views/user/UserDetailsView.vue";
import CreateUserView from "../views/user/CreateUserView.vue";
export default [
  {
    path: "/users",
    name: "users",
    meta: {
      title: "users",
      breadcrumb: [
        {
          text: (route) => "users",
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
      title: "newUser",
      breadcrumb: [
        {
          text: (route) => "users",
          to: "users",
          active: false,
        },
        {
          text: (route) => "newUser",
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
      title: "userDetails",
      breadcrumb: [
        {
          text: (route) => "users",
          to: "users",
          active: false,
        },
        {
          text: (route) => "userDetails",
          to: "user-details",
          active: true,
        },
      ],
    },
    component: UserDetailsView,
  },
];
