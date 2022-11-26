export default {
  install: (app) => {
    // Flowbite init modal
    app.config.globalProperties.$openModal = (ref) => {
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      const modalBack = document.querySelector("[modal-backdrop]");
      if (!modalBack) {
        return mod.show();
      }
    };
    app.config.globalProperties.$hideModal = (ref) => {
      const el = document.getElementById(ref);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      document.querySelector("[modal-backdrop]").remove();
      return mod.hide();
    };

    // Flowbite init tooltip
    app.config.globalProperties.$showTooltip = (ref) => {
      const targetEl = document.getElementById(ref.targetEl);
      const triggerEl = document.getElementById(ref.triggerEl);
      const options = {
        placement: ref.placement || "bottom",
        triggerType: "hover",
      };
      // eslint-disable-next-line no-undef
      const tooltip = new Tooltip(targetEl, triggerEl, options);
      return tooltip.show();
    };

    // Flowbite init dropdown
    app.config.globalProperties.$toggleDropdown = (ref) => {
      const targetEl = document.getElementById(ref.targetEl);
      const triggerEl = document.getElementById(ref.triggerEl);
      const options = {
        placement: ref.placementEl || "bottom",
      };
      const isHidden = targetEl.classList.contains("hidden");
      // eslint-disable-next-line no-undef
      const tooltip = new Dropdown(targetEl, triggerEl, options);
      if (isHidden) return tooltip.show();
      if (!isHidden) return tooltip.hide();
    };
  },
};
