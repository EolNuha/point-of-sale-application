/* eslint-disable no-unused-vars */
const IconsView = () => import("../views/IconsView.vue");
export default [
  {
    path: "/dev/icons",
    name: "icons",
    meta: {
      title: "Icons Page",
      breadcrumb: [
        {
          text: (route) => "Icons",
          to: "icons",
          active: true,
        },
      ],
    },
    component: IconsView,
  },
];
