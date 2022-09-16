import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "./index.css";
import "flowbite";
// import "bootstrap/dist/css/bootstrap.min.css";
// import "bootstrap";
// export const eventBus = createApp(App);
const options = {
  position: "top-right",
  timeout: 100000,
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
createApp(App).use(store).use(router).use(Toast, options).mount("#app");
