/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "axios";

const baseURL = "http://localhost:5000";

export default {
  createOrder({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/orders`,
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
