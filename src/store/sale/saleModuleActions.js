/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  createSale({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/sales`,
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
  getSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getDailySales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales/daily`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data);
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
        .get(`/api/sales/download-exel`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSaleDetails({ commit }, saleId) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales/${saleId}`)
        .then(async (response) => {
          commit("SET_SALE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
