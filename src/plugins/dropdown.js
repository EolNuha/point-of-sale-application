export default {
  install: (app) => {
    app.config.globalProperties.$toggleDropdown = (ref) => {
      const targetEl = document.getElementById(ref.targetEl);
      const triggerEl = document.getElementById(ref.triggerEl);
      const isHidden = targetEl.classList.contains("hidden");
      // eslint-disable-next-line no-undef
      const tooltip = new Dropdown(targetEl, triggerEl);
      if (isHidden) return tooltip.show();
      if (!isHidden) return tooltip.hide();
    };
  },
};
