import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "./index.css";
import "flowbite";
import Icon from "@/components/icons/IconComponent.vue";
import Overlay from "@/components/OverlayComponent.vue";
import Pagination from "@/components/PaginationComponent.vue";
import { useToast } from "vue-toastification";
import openModalPlugin from "./plugins/modals";
import focusPlugin from "./plugins/focus";
import tooltipsPlugin from "./plugins/tooltips";
import debouncePlugin from "./plugins/debounce";
import VueSweetalert2 from "vue-sweetalert2";
import "sweetalert2/dist/sweetalert2.min.css";

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
  .component("IconC", Icon)
  .component("OverlayC", Overlay)
  .component("PaginationC", Pagination);
app
  .use(store)
  .use(router)
  .use(Toast, options)
  .use(VueSweetalert2)
  .use(openModalPlugin)
  .use(focusPlugin)
  .use(tooltipsPlugin)
  .use(debouncePlugin)
  .mount("#app");
