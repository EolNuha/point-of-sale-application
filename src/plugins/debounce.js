export default {
  install: (app) => {
    app.config.globalProperties.$debounce = (func, delayMs) => {
      let timeout = null;
      function createDebounce(func, delayMs) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          func();
        }, delayMs || 500);
      }
      return createDebounce(func, delayMs);
    };
  },
};
