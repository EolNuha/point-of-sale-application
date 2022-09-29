export default {
  install: (app) => {
    app.config.globalProperties.$showTooltip = (ref) => {
      const targetEl = document.getElementById(ref.targetEl);
      const triggerEl = document.getElementById(ref.triggerEl);
      const options = {
        placement: "bottom",
        triggerType: "hover",
        onHide: () => {
          console.log("tooltip is shown");
        },
        onShow: () => {
          console.log("tooltip is hidden");
        },
      };
      // eslint-disable-next-line no-undef
      const tooltip = new Tooltip(targetEl, triggerEl, options);
      return tooltip.show();
    };
  },
};
