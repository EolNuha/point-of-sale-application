export default {
  install: (app) => {
    app.config.globalProperties.$swalConfirmObject = () => {
      return {
        position: "center",
        iconColor: "var(--color-theme-600)",
        confirmButtonText: "Confirm",
        showCancelButton: true,
        showCloseButton: true,
        focusConfirm: true,
        reverseButtons: true,
        customClass: {
          popup: "bg-neutral-300 dark:bg-neutral-700",
          header: "bg-neutral-300 dark:bg-neutral-700",
          confirmButton: "theme-gradient-btn",
          cancelButton: "gray-outline-btn mr-2",
          closeButton:
            "text-gray-400 bg-transparent hover:text-gray-900 text-sm dark:hover:text-white",
        },
        buttonsStyling: false,
      };
    };
  },
};
