/* eslint-disable no-unused-vars */
const NotificationsView = () =>
  import("../views/notifications/NotificationsView.vue");
export default [
  {
    path: "/notifications",
    name: "notifications",
    component: NotificationsView,
    meta: {
      title: "notifications",
      breadcrumb: [
        {
          text: (route) => "notifications",
          to: "notifications",
          active: true,
        },
      ],
    },
  },
];
