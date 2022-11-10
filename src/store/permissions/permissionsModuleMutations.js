export default {
  SET_PERMISSIONS(state, payload) {
    state.permissions = payload;
  },
  SET_PERMISSIONS_ALL(state, payload) {
    state.allPermissions = payload;
  },
};
