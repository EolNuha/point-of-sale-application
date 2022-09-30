/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "axios";

const baseURL = "http://localhost:5000";

export default {
  createPurchase({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases`,
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
};
