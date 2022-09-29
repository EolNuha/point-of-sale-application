export default {
  install: (app) => {
    app.config.globalProperties.$openModal = (ref) => {
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      return mod.show();
    };
    app.config.globalProperties.$hideModal = (ref) => {
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      document.querySelector("[modal-backdrop]").remove();
      return mod.hide();
    };
  },
};
