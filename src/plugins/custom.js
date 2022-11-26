const MONTHS = [
  { id: 0, value: "Custom" },
  { id: 1, value: "january" },
  { id: 2, value: "february" },
  { id: 3, value: "march" },
  { id: 4, value: "april" },
  { id: 5, value: "may" },
  { id: 6, value: "june" },
  { id: 7, value: "july" },
  { id: 8, value: "august" },
  { id: 9, value: "september" },
  { id: 10, value: "october" },
  { id: 11, value: "november" },
  { id: 12, value: "december" },
];

export default {
  install: (app) => {
    app.config.globalProperties.$getMonths = MONTHS;
    app.config.globalProperties.$checkIfMonth = (start, end) => {
      const getMonth = (v) => {
        const month = String(v).padStart(2, "0");
        const year = new Date().getFullYear();
        const days = String(new Date(year, month, 0).getDate()).padStart(
          2,
          "0"
        );

        return {
          startDate: `${year}-${month}-01`,
          endDate: `${year}-${month}-${days}`,
        };
      };
      const monthDates = [];
      for (let i = 0; i < MONTHS.length; i++) {
        monthDates.push(getMonth(i + 1));
      }
      return monthDates.findIndex(
        (el) => el.startDate === start && el.endDate === end
      );
    };
    app.config.globalProperties.$hideAlert = (ref) => {
      const targetEl = document.getElementById(ref.targetEl);
      const triggerEl = document.getElementById(ref.triggerEl);
      const options = {
        triggerEl: triggerEl,
        transition: "transition-opacity",
        duration: 200,
        timing: "ease-out",
      };
      // eslint-disable-next-line no-undef
      const dismiss = new Dismiss(targetEl, options);
      dismiss.hide();
    };
  },
};
