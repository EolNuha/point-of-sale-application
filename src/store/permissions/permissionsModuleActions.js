/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getUserPermissions({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/permissions`, { params: data })
        .then(async (response) => {
          commit("SET_PERMISSIONS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllPermissions({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/permissions/all`, { params: data })
        .then(async (response) => {
          commit("SET_PERMISSIONS_ALL", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getUserTypePermissions({ commit }, type) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/permissions/${type}`)
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updatePermission({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/permissions`,
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
};
