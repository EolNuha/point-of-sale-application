/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/sales`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/purchases`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductsSoldbyAmount({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products-sold-by-amount`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCTS_SOLD_BY_AMOUNT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products/${data.id}`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCT_STATS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
