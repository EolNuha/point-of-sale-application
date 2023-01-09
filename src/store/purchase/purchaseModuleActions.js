/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  createPurchase({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases`,
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
  getPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchasesDetailed({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases-detailed`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllPurchasesDetailed({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases-detailed`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getDailyPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/daily`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllDailyPurchases({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/daily`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchaseDetails({ commit }, purchaseId) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/${purchaseId}`)
        .then(async (response) => {
          commit("SET_PURCHASE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSellers({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sellers`, { params: data })
        .then(async (response) => {
          commit("SET_SELLERS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSellerDetails({ commit }, sellerName) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sellers/${sellerName}`)
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updatePurchase({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases/${data.id}`,
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
  deletePurchase({ commit, state }, id) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/purchases/${id}`,
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
};
