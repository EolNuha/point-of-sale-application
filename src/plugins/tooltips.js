export default {
  install: (app) => {
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
  },
};
