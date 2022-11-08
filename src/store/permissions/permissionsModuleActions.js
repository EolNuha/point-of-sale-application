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
};
