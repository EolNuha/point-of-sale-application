export default {
  methods: {
    tableToExcel(table, fileName) {
      let uri =
          "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,",
        template =
          '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="https://www.w3.org/TR/html40/"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>eol</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>',
        base64 = function (s) {
          return window.btoa(unescape(encodeURIComponent(s)));
        },
        format = function (s, c) {
          return s.replace(/{(\w+)}/g, function (m, p) {
            return c[p];
          });
        };
      let ctx = {
        worksheet: "Worksheet",
        table: table.innerHTML,
      };
      let a = document.createElement("a");
      a.href = uri + base64(format(template, ctx));
      a.download = `${fileName}.xlsx`;
      a.click();
    },
  },
};
