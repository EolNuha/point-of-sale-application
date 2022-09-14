import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./index.css";
import "flowbite";
// import "bootstrap/dist/css/bootstrap.min.css";
// import "bootstrap";

createApp(App).use(store).use(router).mount("#app");
