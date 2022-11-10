/* eslint-disable no-unused-vars */
const SettingsView = () => import("../views/settings/SettingsView.vue");
const LanguagesView = () => import("../views/settings/LanguagesView.vue");
const ThemeView = () => import("../views/settings/ThemeView.vue");
const PermissionsView = () => import("../views/settings/PermissionsView.vue");
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
  {
    path: "/settings/theme",
    name: "theme",
    component: ThemeView,
    meta: {
      title: "theme",
      breadcrumb: [
        {
          text: (route) => "settings",
          to: "settings",
          active: false,
        },
        {
          text: (route) => "theme",
          to: "theme",
          active: true,
        },
      ],
    },
  },
  {
    path: "/settings/permissions",
    name: "permissions",
    component: PermissionsView,
    meta: {
      title: "permissions",
      breadcrumb: [
        {
          text: (route) => "settings",
          to: "settings",
          active: false,
        },
        {
          text: (route) => "permissions",
          to: "permissions",
          active: true,
        },
      ],
    },
  },
];
