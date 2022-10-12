/* eslint-disable no-unused-vars */
import IconsView from "../views/IconsView.vue";
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
