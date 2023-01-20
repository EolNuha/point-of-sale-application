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
  updateNotifications({ commit, dispatch }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/notifications`,
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
  deleteNotifications({ commit, dispatch }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/notifications`,
        method: "DELETE",
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
  deleteNotification({ commit, dispatch }, id) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/notifications/${id}`,
        method: "DELETE",
      })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getNotificationsList({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/notifications`, { params: data })
        .then(async (response) => {
          commit("SET_NOTIFICATIONS_LIST", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updateNotification({ commit, dispatch }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/notifications/${data.id}`,
        method: "POST",
        data,
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
