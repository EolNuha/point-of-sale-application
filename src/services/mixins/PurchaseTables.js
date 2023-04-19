export default {
  methods: {
    getTableTaxValue(taxArr, taxAlias, taxProp) {
      const arr = JSON.parse(JSON.stringify(taxArr));
      const obj = Array.isArray(arr)
        ? arr?.find((obj) => obj.taxAlias === taxAlias)
        : 0;
      return typeof obj === "object" ? obj[taxProp] : 0;
    },
    getGridTaxValue(taxArr, taxAlias, taxProp) {
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
        let totalWOTaxTh = document.createElement("th");
        totalWOTaxTh.innerHTML = `${this.$t("subTotal")} ${tax.settingsName}%`;
        headTr.appendChild(totalWOTaxTh);
      }

      let woTaxTh = document.createElement("th");
      woTaxTh.innerHTML = this.$t("purchaseWithoutTax");
      headTr.appendChild(woTaxTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("totalAmount");
      headTr.appendChild(totalTh);

      let totalTaxTh = document.createElement("th");
      totalTaxTh.innerHTML = this.$t("totalTaxAmount");
      headTr.appendChild(totalTaxTh);

      for await (const element of this.allPurchases) {
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
          let totalWOTaxTd = document.createElement("td");
          totalWOTaxTd.innerHTML = `${this.getTableTaxValue(
            element.taxes,
            tax.settingsAlias,
            "totalWithoutTax"
          )}`;
          bodyTr.appendChild(totalWOTaxTd);
        }
        let woTaxTd = document.createElement("td");
        woTaxTd.innerHTML = `${this.getTableTaxValue(
          element.taxes,
          "zero",
          "totalWithoutTax"
        )}`;
        bodyTr.appendChild(woTaxTd);
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.totalAmount}`;
        bodyTr.appendChild(totalTd);
        let totalTaxTd = document.createElement("td");
        totalTaxTd.innerHTML = `${element.totalTaxAmount}`;
        bodyTr.appendChild(totalTaxTd);
        tbody.appendChild(bodyTr);
      }

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

      // let idTh = document.createElement("th");
      // idTh.innerHTML = "ID";
      // headTr.appendChild(idTh);

      let sellerNameTh = document.createElement("th");
      sellerNameTh.innerHTML = this.$t("sellerName");
      headTr.appendChild(sellerNameTh);

      let invoiceTh = document.createElement("th");
      invoiceTh.innerHTML = this.$t("invoiceNumber");
      headTr.appendChild(invoiceTh);

      let fiscalTh = document.createElement("th");
      fiscalTh.innerHTML = this.$t("fiscalNumber");
      headTr.appendChild(fiscalTh);

      let taxTh = document.createElement("th");
      taxTh.innerHTML = this.$t("taxNumber");
      headTr.appendChild(taxTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("th");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
        let totalWOTaxTh = document.createElement("th");
        totalWOTaxTh.innerHTML = `${this.$t("subTotal")} ${tax.settingsName}%`;
        headTr.appendChild(totalWOTaxTh);
      }

      let woTaxTh = document.createElement("th");
      woTaxTh.innerHTML = this.$t("purchaseWithoutTax");
      headTr.appendChild(woTaxTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("totalAmount");
      headTr.appendChild(totalTh);

      let totalTaxTh = document.createElement("th");
      totalTaxTh.innerHTML = this.$t("totalTaxAmount");
      headTr.appendChild(totalTaxTh);

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.dateCreated?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        // let idTd = document.createElement("td");
        // idTd.innerHTML = element.id;
        // bodyTr.appendChild(idTd);

        let sellerNameTd = document.createElement("td");
        sellerNameTd.innerHTML = element.sellerName;
        bodyTr.appendChild(sellerNameTd);

        let invoiceTd = document.createElement("td");
        invoiceTd.innerHTML = element.sellerInvoiceNumber;
        bodyTr.appendChild(invoiceTd);

        let fiscalTd = document.createElement("td");
        fiscalTd.innerHTML = element.sellerFiscalNumber;
        bodyTr.appendChild(fiscalTd);

        let taxTd = document.createElement("td");
        taxTd.innerHTML = element.sellerTaxNumber;
        bodyTr.appendChild(taxTd);

        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getGridTaxValue(
            element.taxes,
            tax.settingsAlias,
            "taxValue"
          )}`;
          bodyTr.appendChild(taxTd);
          let totalWOTaxTd = document.createElement("td");
          totalWOTaxTd.innerHTML = `${this.getGridTaxValue(
            element.taxes,
            tax.settingsAlias,
            "totalWithoutTax"
          )}`;
          bodyTr.appendChild(totalWOTaxTd);
        }
        let woTaxTd = document.createElement("td");
        woTaxTd.innerHTML = `${this.getGridTaxValue(
          element.taxes,
          "zero",
          "totalWithoutTax"
        )}`;
        bodyTr.appendChild(woTaxTd);
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.totalAmount}`;
        bodyTr.appendChild(totalTd);
        let totalTaxTd = document.createElement("td");
        totalTaxTd.innerHTML = `${element.totalTaxAmount}`;
        bodyTr.appendChild(totalTaxTd);
        tbody.appendChild(bodyTr);
      }

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);

      return table;
    },
  },
};
