export default {
  SET_USERS(state, data) {
    state.users = data;
  },
  SET_PAGINATION(state, data) {
    state.pagination = data;
  },
  SET_CURRENT_USER(state, data) {
    state.currentUser = data;
  },
  SET_USER(state, data) {
    state.user = data;
  },
};
