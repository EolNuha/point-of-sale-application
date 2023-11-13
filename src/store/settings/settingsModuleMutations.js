export default {
  SET_SETTINGS_TYPE(state, { data, settingsType }) {
    state.settings_type[settingsType] = data;
  },
};
