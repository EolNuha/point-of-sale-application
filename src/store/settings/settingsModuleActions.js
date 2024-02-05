/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getSettingsType({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/settings/${data.settings_type}`)
        .then(async (response) => {
          commit("SET_SETTINGS_TYPE", {
            data: response.data,
            settingsType: data.settings_type,
          });
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updateCompany({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/settings/company`,
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
  getCompany({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/settings/company`)
        .then(async (response) => {
          resolve(response);
          commit("SET_COMPANY", response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
