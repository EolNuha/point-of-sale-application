export default {
  methods: {
    getTableTaxValue(taxArr, tax_alias, taxProp) {
      const arr = JSON.parse(JSON.stringify(taxArr));
      const obj = Array.isArray(arr)
        ? arr?.find((obj) => obj.tax_alias === tax_alias)
        : 0;
      return typeof obj === "object" ? obj[taxProp] : 0;
    },
    getGridTaxValue(taxArr, tax_alias, taxProp) {
      const arr = JSON.parse(JSON.stringify(taxArr));
      const obj = arr ? arr[tax_alias] : 0;
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
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settings_name}%`;
        headTr.appendChild(taxTh);
        let totalWOTaxTh = document.createElement("th");
        totalWOTaxTh.innerHTML = `${this.$t("subTotal")} ${tax.settings_name}%`;
        headTr.appendChild(totalWOTaxTh);
      }

      let woTaxTh = document.createElement("th");
      woTaxTh.innerHTML = this.$t("purchaseWithoutTax");
      headTr.appendChild(woTaxTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("total_amount");
      headTr.appendChild(totalTh);

      let totalTaxTh = document.createElement("th");
      totalTaxTh.innerHTML = this.$t("total_tax_amount");
      headTr.appendChild(totalTaxTh);

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.date_created?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getTableTaxValue(
            element.taxes,
            tax.settings_alias,
            "tax_value"
          )}`;
          bodyTr.appendChild(taxTd);
          let totalWOTaxTd = document.createElement("td");
          totalWOTaxTd.innerHTML = `${this.getTableTaxValue(
            element.taxes,
            tax.settings_alias,
            "total_without_tax"
          )}`;
          bodyTr.appendChild(totalWOTaxTd);
        }
        let woTaxTd = document.createElement("td");
        woTaxTd.innerHTML = `${this.getTableTaxValue(
          element.taxes,
          "zero",
          "total_without_tax"
        )}`;
        bodyTr.appendChild(woTaxTd);
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.total_amount}`;
        bodyTr.appendChild(totalTd);
        let totalTaxTd = document.createElement("td");
        totalTaxTd.innerHTML = `${element.total_tax_amount}`;
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

      let seller_nameTh = document.createElement("th");
      seller_nameTh.innerHTML = this.$t("seller_name");
      headTr.appendChild(seller_nameTh);

      let invoiceTh = document.createElement("th");
      invoiceTh.innerHTML = this.$t("invoice_number");
      headTr.appendChild(invoiceTh);

      let fiscalTh = document.createElement("th");
      fiscalTh.innerHTML = this.$t("fiscal_number");
      headTr.appendChild(fiscalTh);

      let taxTh = document.createElement("th");
      taxTh.innerHTML = this.$t("tax_number");
      headTr.appendChild(taxTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("th");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settings_name}%`;
        headTr.appendChild(taxTh);
        let totalWOTaxTh = document.createElement("th");
        totalWOTaxTh.innerHTML = `${this.$t("subTotal")} ${tax.settings_name}%`;
        headTr.appendChild(totalWOTaxTh);
      }

      let woTaxTh = document.createElement("th");
      woTaxTh.innerHTML = this.$t("purchaseWithoutTax");
      headTr.appendChild(woTaxTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("total_amount");
      headTr.appendChild(totalTh);

      let totalTaxTh = document.createElement("th");
      totalTaxTh.innerHTML = this.$t("total_tax_amount");
      headTr.appendChild(totalTaxTh);

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.date_created?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        // let idTd = document.createElement("td");
        // idTd.innerHTML = element.id;
        // bodyTr.appendChild(idTd);

        let seller_nameTd = document.createElement("td");
        seller_nameTd.innerHTML = element.seller_name;
        bodyTr.appendChild(seller_nameTd);

        let invoiceTd = document.createElement("td");
        invoiceTd.innerHTML = element.seller_invoice_number;
        bodyTr.appendChild(invoiceTd);

        let fiscalTd = document.createElement("td");
        fiscalTd.innerHTML = element.seller_fiscal_number;
        bodyTr.appendChild(fiscalTd);

        let taxTd = document.createElement("td");
        taxTd.innerHTML = element.seller_tax_number;
        bodyTr.appendChild(taxTd);

        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getGridTaxValue(
            element.taxes,
            tax.settings_alias,
            "tax_value"
          )}`;
          bodyTr.appendChild(taxTd);
          let totalWOTaxTd = document.createElement("td");
          totalWOTaxTd.innerHTML = `${this.getGridTaxValue(
            element.taxes,
            tax.settings_alias,
            "total_without_tax"
          )}`;
          bodyTr.appendChild(totalWOTaxTd);
        }
        let woTaxTd = document.createElement("td");
        woTaxTd.innerHTML = `${this.getGridTaxValue(
          element.taxes,
          "zero",
          "total_without_tax"
        )}`;
        bodyTr.appendChild(woTaxTd);
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.total_amount}`;
        bodyTr.appendChild(totalTd);
        let totalTaxTd = document.createElement("td");
        totalTaxTd.innerHTML = `${element.total_tax_amount}`;
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
