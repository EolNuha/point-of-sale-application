/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getSales({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/sales`, { params: data })
        .then(async (response) => {
          commit("SET_SALES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSalesGrossProfit({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/sales-gross-profit`, { params: data })
        .then(async (response) => {
          commit("SET_SALES_GROSS_PROFIT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSaleStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/sales/${data.startDate}`)
        .then(async (response) => {
          commit("SET_SALE_STATS", response.data);
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
        .get(`/api/analytics/purchases`, { params: data })
        .then(async (response) => {
          commit("SET_PURCHASES", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getPurchaseStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/purchases/${data.startDate}`)
        .then(async (response) => {
          commit("SET_PURCHASE_STATS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductsSoldbyAmount({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products-sold-by-amount`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCTS_SOLD_BY_AMOUNT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductsbyGrossProfit({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products-sold-by-gross-profit`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCTS_SOLD_BY_GROSS_PROFIT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductsbyNetProfit({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products-sold-by-net-profit`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCTS_SOLD_BY_NET_PROFIT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/products/${data.id}`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCT_STATS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getUsersSaleRevenue({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/users-revenue`, { params: data })
        .then(async (response) => {
          commit("SET_USERS_REVENUE", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getUserStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/users/${data.id}`, { params: data })
        .then(async (response) => {
          commit("SET_USER_STATS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getSellerStats({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/analytics/sellers/${data.id}`, { params: data })
        .then(async (response) => {
          commit("SET_SELLER_STATS", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
