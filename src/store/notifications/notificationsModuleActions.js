/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getNotifications({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/notifications`, { params: data })
        .then(async (response) => {
          commit("SET_NOTIFICATIONS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  checkProductExpiration({ commit, dispatch }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/notifications/product-expire`, { params: data })
        .then(async (response) => {
          dispatch("getNotifications");
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updateNotification({ commit, dispatch }, id) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/notifications/${id}`,
        method: "POST",
        data: { read: true },
      })
        .then(async (response) => {
          dispatch("getNotifications");
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
