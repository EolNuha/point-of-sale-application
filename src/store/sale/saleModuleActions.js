/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  createSale({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/sales`,
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
  getSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSalesDetailed({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales-detailed`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllSalesDetailed({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales-detailed`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getDailySales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales/daily`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllDailySales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales/daily`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSaleDetails({ commit }, saleId) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/sales/${saleId}`)
        .then(async (response) => {
          commit("SET_SALE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  updateSale({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/sales/${data.id}`,
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
  deleteSale({ commit, state }, id) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/sales/${id}`,
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
