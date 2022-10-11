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
};
