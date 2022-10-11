/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import { createStore } from "vuex";
import productModule from "./product/productModule";
import saleModule from "./sale/saleModule";
import purchaseModule from "./purchase/purchaseModule";
import userModule from "./user/userModule";
import analyticsModule from "./analytics/analyticsModule";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    productModule,
    saleModule,
    purchaseModule,
    userModule,
    analyticsModule,
  },
});
