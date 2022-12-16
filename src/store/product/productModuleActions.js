/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import axios from "../axiosAuth";

export default {
  getProducts({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/products`, { params: data })
        .then(async (response) => {
          commit("SET_PRODUCTS", response.data.data);
          commit("SET_PAGINATION", response.data.pagination);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getAllProducts({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/products`, { params: data })
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductDetails({ commit }, productId) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/products/${productId}`)
        .then(async (response) => {
          commit("SET_PRODUCT", response.data);
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  createProduct({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/products`,
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
  updateProduct({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/products/${data.id}`,
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
  deleteProducts({ commit }, data) {
    return new Promise((resolve, reject) => {
      axios({
        url: `/api/products`,
        method: "DELETE",
        data,
      })
        .then((response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  deleteProduct({ commit }, productId) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/products/${productId}`)
        .then((response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  getProductDetailsByBarcode({ commit }, productBarcode) {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/products/barcode/${productBarcode}`)
        .then(async (response) => {
          resolve(response);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
