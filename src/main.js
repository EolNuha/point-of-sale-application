import { createApp } from "vue";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "./index.css";
import "flowbite";
import { useToast } from "vue-toastification";
import VueSweetalert2 from "vue-sweetalert2";
import "sweetalert2/dist/sweetalert2.min.css";
import "vue-select/dist/vue-select.css";
import VueApexCharts from "vue3-apexcharts";
import registerComponents from "./global-components";
import registerPlugins from "./global-plugins";
import en from "./langs/en.json";
import sq from "./langs/sq.json";
// import Vue3Tour from "vue3-tour";
import { abilitiesPlugin } from "@casl/vue";
import ability from "./services/ability";
// import "vue3-tour/dist/vue3-tour.css";

const messages = {
  en: en,
  sq: sq,
};

const i18n = createI18n({
  locale: "en", // set locale
  fallbackLocale: "en", // set fallback locale
  messages, // set locale messages
});

const app = createApp(App);
app.config.globalProperties.$toast = useToast();
const options = {
  position: "top-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  newestOnTop: true,
  hideProgressBar: true,
  maxToasts: 2,
  closeButton: "button",
  icon: true,
  rtl: false,
};
app
  .use(store)
  .use(router)
  .use(Toast, options)
  .use(i18n)
  .use(VueSweetalert2)
  // .use(Vue3Tour)
  .use(VueApexCharts)
  .use(abilitiesPlugin, ability, {
    useGlobalProperties: true,
  });

registerComponents(app);
registerPlugins(app);

app.mount("#app");
