/* eslint-disable no-unused-vars */
const SettingsView = () => import("../views/settings/SettingsView.vue");
const LanguagesView = () => import("../views/settings/LanguagesView.vue");
export default [
  {
    path: "/settings",
    name: "settings",
    component: SettingsView,
    meta: {
      title: "settings",
      breadcrumb: [
        {
          text: (route) => "settings",
          to: "settings",
          active: true,
        },
      ],
    },
  },
  {
    path: "/settings/languages",
    name: "languages",
    component: LanguagesView,
    meta: {
      title: "languages",
      breadcrumb: [
        {
          text: (route) => "settings",
          to: "settings",
          active: false,
        },
        {
          text: (route) => "languages",
          to: "languages",
          active: true,
        },
      ],
    },
  },
];
