export default {
  SET_USERS(state, payload) {
    state.users = payload;
  },
  SET_CURRENT_USER(state, payload) {
    state.currentUser = payload;
  },
  SET_USER(state, payload) {
    state.user = payload;
  },
};