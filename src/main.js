import { createApp } from "vue";
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
  hideProgressBar: true,
  closeButton: "button",
  icon: true,
  rtl: false,
};
app
  .use(store)
  .use(router)
  .use(Toast, options)
  .use(VueSweetalert2)
  .use(VueApexCharts);

registerComponents(app);
registerPlugins(app);

app.mount("#app");
