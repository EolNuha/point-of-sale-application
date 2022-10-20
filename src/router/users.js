/* eslint-disable no-unused-vars */
const UsersView = () => import("../views/user/UsersView.vue");
const UserDetailsView = () => import("../views/user/UserDetailsView.vue");
const CreateUserView = () => import("../views/user/CreateUserView.vue");
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
