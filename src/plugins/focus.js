export default {
  install: (app) => {
    app.config.globalProperties.$putOnFocus = (ref) => {
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      return el?.focus();
    };
  },
};
