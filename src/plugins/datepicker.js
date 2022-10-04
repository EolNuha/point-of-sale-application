import DateRangePicker from "flowbite-datepicker/DateRangePicker";

export default {
  install: (app) => {
    app.config.globalProperties.$dateRangePicker = (ref) => {
      const dateRangePickerEl = document.getElementById(ref);
      new DateRangePicker(dateRangePickerEl, {
        clearBtn: true,
        format: "dd/mm/yy",
      });
    };
  },
};
