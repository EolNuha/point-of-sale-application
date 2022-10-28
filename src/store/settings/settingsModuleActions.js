/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getSettingsType({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/settings/${data.settingsType}`, { params: data })
        .then(async (response) => {
          commit("SET_SETTINGS_TYPE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
