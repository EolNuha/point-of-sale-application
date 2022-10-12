/* eslint-disable no-unused-vars */
import NotFound from "../views/errors/404View.vue";
export default [
  {
    path: "/404",
    name: "404",
    component: NotFound,
    meta: {
      title: "Error 404 Page",
      breadcrumb: [
        {
          text: (route) => "Error 404 Page",
          to: "404",
          active: true,
        },
      ],
    },
  },
];
