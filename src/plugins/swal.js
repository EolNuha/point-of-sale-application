export default {
  install: (app) => {
    app.config.globalProperties.$swalConfirmObject = () => {
      return {
        position: "center",
        iconColor: "#1c64f2",
        confirmButtonText: "Confirm",
        showCancelButton: true,
        showCloseButton: true,
        focusConfirm: true,
        reverseButtons: true,
        customClass: {
          popup: "bg-gray-300 dark:bg-gray-700",
          header: "bg-gray-300 dark:bg-gray-700",
          confirmButton: "blue-gradient-btn",
          cancelButton: "gray-outline-btn mr-2",
          closeButton:
            "text-gray-400 bg-transparent hover:text-gray-900 text-sm dark:hover:text-white",
        },
        buttonsStyling: false,
      };
    };
  },
};
