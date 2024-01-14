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
        .get(`/api/purchases/grouped`, { params: data })
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
        .get(`/api/purchases/detailed`, { params: data })
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
  getPurchasesGroupedExcel({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/grouped/excel`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchasesDetailedExcel({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/detailed/excel`, {
          params: data,
          responseType: "blob",
        })
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
  getDailyPurchasesExcel({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/purchases/daily/excel`, { params: data })
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
  getSellerDetails({ commit }, seller_name) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sellers/${seller_name}`)
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
