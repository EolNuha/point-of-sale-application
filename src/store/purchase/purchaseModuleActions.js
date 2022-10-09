/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  createPurchase({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases`,
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
        .get(`/api/purchases`, { params: data })
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
        .get(`/api/purchases/download-exel`, { params: data })
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
        .get(`/api/purchases/${purchaseId}`)
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
        .get(`/api/sellers/${sellerName}`)
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
