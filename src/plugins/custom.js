const MONTHS = [
  { id: 0, value: "Custom" },
  { id: 1, value: "January" },
  { id: 2, value: "February" },
  { id: 3, value: "March" },
  { id: 4, value: "April" },
  { id: 5, value: "May" },
  { id: 6, value: "June" },
  { id: 7, value: "July" },
  { id: 8, value: "August" },
  { id: 9, value: "September" },
  { id: 10, value: "October" },
  { id: 11, value: "November" },
  { id: 12, value: "December" },
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
  },
};
