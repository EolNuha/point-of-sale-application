export default {
  install: (app) => {
    // inject a globally available $translate() method
    app.config.globalProperties.$openModal = (ref) => {
      // retrieve a nested property in `options`
      // using `key` as the path
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      return mod.show();
    };
    app.config.globalProperties.$hideModal = (ref) => {
      // retrieve a nested property in `options`
      // using `key` as the path
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      document.querySelector("[modal-backdrop]").remove();
      return mod.hide();
    };
  },
};
