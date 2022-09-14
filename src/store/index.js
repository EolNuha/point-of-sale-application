import { createStore } from "vuex";
import axios from "axios";

const baseURL = "http://127.0.0.1:5000";

export default createStore({
  state: { testVar: 3, something: [] },
  getters: {},
  mutations: {
    INCREMENT_COUNT(state, payload) {
      state.testVar += payload;
    },
    SET_SOMETHING(state, payload) {
      state.something = payload;
    },
  },
  actions: {
    getSomething({ commit }) {
      return new Promise((resolve, reject) => {
        axios
          .get(`${baseURL}/test`)
          .then(async (response) => {
            commit("SET_SOMETHING", response.data);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },
  modules: {},
});
