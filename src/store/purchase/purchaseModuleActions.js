/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "axios";

const baseURL = "http://localhost:5000";

export default {
  createPurchase({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases`,
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
  getPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${baseURL}/api/purchases`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  downloadExcelFile({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${baseURL}/api/purchases/download-exel`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchaseDetails({ commit }, purchaseId) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${baseURL}/api/purchases/${purchaseId}`)
        .then(async (response) => {
          commit("SET_PURCHASE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSellerDetails({ commit }, sellerName) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${baseURL}/api/sellers/${sellerName}`)
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
