/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000";
axios.defaults.headers.common["x-access-token"] = `${sessionStorage.getItem(
  "token"
)}`;

export default {
  getUsers({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/users`, {
          params: data,
        })
        .then(async (response) => {
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
        url: `/sigin`,
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
