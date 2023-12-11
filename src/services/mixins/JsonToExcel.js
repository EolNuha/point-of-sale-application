import { utils, writeFile } from "xlsx";

export default {
  methods: {
    translateObjectKeys(obj) {
      const translatedObject = {};

      for (const key in obj) {
        // eslint-disable-next-line no-prototype-builtins
        if (obj.hasOwnProperty(key)) {
          translatedObject[this.$t(key)] = obj[key]; // Assuming obj[key] is the translation key
        }
      }

      return translatedObject;
    },
    async jsonToExcel(jsonData, fileName) {
      const workbook = utils.book_new();
      const translatedArray = jsonData.map(this.translateObjectKeys);

      // Convert the JSON data to a worksheet
      const worksheet = utils.json_to_sheet(translatedArray);

      // Add the worksheet to the workbook
      utils.book_append_sheet(workbook, worksheet, "Sheet1");

      // Write the workbook to a file
      await writeFile(workbook, `${fileName}.xlsx`);
    },
  },
};
