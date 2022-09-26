/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import { createStore } from "vuex";
import productModule from "./product/productModule";
import orderModule from "./order/orderModule";

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: { productModule, orderModule },
});
