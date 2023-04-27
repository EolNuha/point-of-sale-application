export default {
  methods: {
    getTableTaxValue(taxArr, taxAlias, taxProp) {
      console.log(taxArr);
      const arr = JSON.parse(JSON.stringify(taxArr));
      const obj = Array.isArray(arr)
        ? arr?.find((obj) => obj.taxAlias === taxAlias)
        : 0;
      return typeof obj === "object" ? obj[taxProp] : 0;
    },
    getGridTaxValue(taxArr, taxAlias, taxProp) {
      console.log(taxArr);
      const arr = JSON.parse(JSON.stringify(taxArr));
      const obj = arr ? arr[taxAlias] : 0;
      return typeof obj === "object" ? obj[taxProp] : 0;
    },
    async tableExcelView() {
      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let dateTh = document.createElement("th");
      dateTh.innerHTML = this.$t("date");
      headTr.appendChild(dateTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("th");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }
      for await (const item of [
        "subtotalAmount",
        "totalAmount",
        "grossProfit",
        "netProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = this.$t(item);
        headTr.appendChild(itemTh);
      }

      for await (const element of this.allSales.data) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.dateCreated?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getTableTaxValue(
            element.taxes,
            tax.settingsAlias,
            "taxValue"
          )}`;
          bodyTr.appendChild(taxTd);
        }
        for await (const item of [
          "subTotalAmount",
          "totalAmount",
          "grossProfitAmount",
          "netProfitAmount",
        ]) {
          let itemTd = document.createElement("td");
          itemTd.innerHTML = `${element[item]}`;
          bodyTr.appendChild(itemTd);
        }
        tbody.appendChild(bodyTr);
      }

      let totalTr = document.createElement("tr");
      let bottomTd = document.createElement("th");
      bottomTd.innerHTML = this.$t("total");
      totalTr.appendChild(bottomTd);
      for await (const tax of this.allSales.pagination.taxes) {
        let taxTd = document.createElement("th");
        taxTd.innerHTML = `${tax.taxValue}`;
        totalTr.appendChild(taxTd);
      }
      for await (const item of [
        "salesSubTotalAmount",
        "salesTotalAmount",
        "salesTotalGrossProfit",
        "salesTotalNetProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = `${this.allSales.pagination[item]}`;
        totalTr.appendChild(itemTh);
      }

      tbody.appendChild(totalTr);

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);

      return table;
    },
    async gridExcelView() {
      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let dateTh = document.createElement("th");
      dateTh.innerHTML = this.$t("date");
      headTr.appendChild(dateTh);

      let idTh = document.createElement("th");
      idTh.innerHTML = "ID";
      headTr.appendChild(idTh);

      let employeeTh = document.createElement("th");
      employeeTh.innerHTML = this.$t("employee");
      headTr.appendChild(employeeTh);

      let typeTh = document.createElement("th");
      typeTh.innerHTML = this.$t("type");
      headTr.appendChild(typeTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("th");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }
      for await (const item of [
        "subtotalAmount",
        "totalAmount",
        "grossProfit",
        "netProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = this.$t(item);
        headTr.appendChild(itemTh);
      }

      for await (const element of this.allSales.data) {
        let bodyTr = document.createElement("tr");

        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.dateCreated?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        let idTd = document.createElement("td");
        idTd.innerHTML = element.id;
        bodyTr.appendChild(idTd);
        let employeeTd = document.createElement("td");
        employeeTd.innerHTML = `${element.user.firstName} ${element.user.lastName}`;
        bodyTr.appendChild(employeeTd);
        let typeTd = document.createElement("td");
        typeTd.innerHTML = element.isRegular
          ? this.$t("regular")
          : this.$t("irregular");
        bodyTr.appendChild(typeTd);

        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getGridTaxValue(
            element.taxes,
            tax.settingsAlias,
            "taxValue"
          )}`;
          bodyTr.appendChild(taxTd);
        }

        for await (const item of [
          "subTotalAmount",
          "totalAmount",
          "grossProfitAmount",
          "netProfitAmount",
        ]) {
          let itemTd = document.createElement("td");
          itemTd.innerHTML = `${element[item]}`;
          bodyTr.appendChild(itemTd);
        }
        tbody.appendChild(bodyTr);
      }

      let totalTr = document.createElement("tr");
      let bottomTd = document.createElement("th");
      bottomTd.innerHTML = this.$t("total");
      totalTr.appendChild(bottomTd);
      let emptyTd = document.createElement("th");
      emptyTd.innerHTML = "-";
      totalTr.appendChild(emptyTd);
      let empty1Td = document.createElement("th");
      empty1Td.innerHTML = "-";
      totalTr.appendChild(empty1Td);
      let empty2Td = document.createElement("th");
      empty2Td.innerHTML = "-";
      totalTr.appendChild(empty2Td);
      for await (const tax of this.allSales.pagination.taxes) {
        let taxTd = document.createElement("th");
        taxTd.innerHTML = `${tax.taxValue}`;
        totalTr.appendChild(taxTd);
      }
      for await (const item of [
        "salesSubTotalAmount",
        "salesTotalAmount",
        "salesTotalGrossProfit",
        "salesTotalNetProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = `${this.allSales.pagination[item]}`;
        totalTr.appendChild(itemTh);
      }

      tbody.appendChild(totalTr);

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);

      return table;
    },
  },
};
