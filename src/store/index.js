/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import { createStore } from "vuex";
import axios from "axios";

const baseURL = "http://localhost:5000";

export default createStore({
  state: { products: [], product: {} },
  getters: {},
  mutations: {
    SET_PRODUCTS(state, payload) {
      state.products = payload;
    },
    SET_PRODUCT(state, payload) {
      state.product = payload;
    },
  },
  actions: {
    getProducts({ commit }) {
      return new Promise((resolve, reject) => {
        axios
          .get(`${baseURL}/api/products`)
          .then(async (response) => {
            commit("SET_PRODUCTS", response.data);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    getProductDetails({ commit }, productId) {
      return new Promise((resolve, reject) => {
        axios
          .get(`${baseURL}/api/products/${productId}`)
          .then(async (response) => {
            commit("SET_PRODUCT", response.data);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    createProduct({ commit, state }, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `/api/products`,
          baseURL,
          method: "POST",
          data,
        })
          .then(async (response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    updateProduct({ commit, state }, data) {
      return new Promise((resolve, reject) => {
        axios({
          url: `/api/products/${data.id}`,
          baseURL,
          method: "POST",
          data,
        })
          .then(async (response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    deleteProduct({ commit }, productId) {
      return new Promise((resolve, reject) => {
        axios
          .delete(`${baseURL}/api/products/${productId}`)
          .then((response) => {
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },
  modules: {},
});
