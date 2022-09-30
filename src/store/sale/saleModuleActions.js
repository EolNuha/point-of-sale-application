/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "axios";

const baseURL = "http://localhost:5000";

export default {
  createSale({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/sales`,
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
  getSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`${baseURL}/api/sales`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data);
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
        .get(`${baseURL}/api/sales/${saleId}`)
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
