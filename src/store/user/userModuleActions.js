/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getUsers({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/users`, {
          params: data,
        })
        .then(async (response) => {
          resolve(response);
          commit("SET_USERS", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updateUserDetails({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/users/${data.id}`,
        method: "PUT",
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
  getUserDetails({ commit, state }, userId) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/users/${userId}`,
        method: "GET",
      })
        .then(async (response) => {
          resolve(response);
          commit("SET_USER", response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  deleteUser({ commit }, userId) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/users/${userId}`)
        .then((response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getCurrentUser({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/current-user`,
        method: "GET",
        data,
      })
        .then(async (response) => {
          resolve(response);
          commit("SET_CURRENT_USER", response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  signinUser({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/signin`,
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
  createUser({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/signup`,
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
};
