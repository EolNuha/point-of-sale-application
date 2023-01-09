export default {
  methods: {
    async tableExcelView() {
      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let dateTh = document.createElement("th");
      dateTh.innerHTML = this.$t("date");
      headTr.appendChild(dateTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("td");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }

      let subtotalTh = document.createElement("th");
      subtotalTh.innerHTML = this.$t("subtotalAmount");
      headTr.appendChild(subtotalTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("totalAmount");
      headTr.appendChild(totalTh);

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.dateCreated?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getTaxValue(
            element.taxes,
            tax.settingsAlias
          )} €`;
          bodyTr.appendChild(taxTd);
        }
        let subtotalTd = document.createElement("td");
        subtotalTd.innerHTML = `${element.subTotalAmount} €`;
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.totalAmount} €`;
        bodyTr.appendChild(subtotalTd);
        bodyTr.appendChild(totalTd);
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

      let idTh = document.createElement("th");
      idTh.innerHTML = "ID";
      headTr.appendChild(idTh);

      let sellerNameTh = document.createElement("th");
      sellerNameTh.innerHTML = this.$t("sellerName");
      headTr.appendChild(sellerNameTh);

      let invoiceTh = document.createElement("th");
      invoiceTh.innerHTML = this.$t("invoiceNumber");
      headTr.appendChild(invoiceTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("td");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }

      let subtotalTh = document.createElement("th");
      subtotalTh.innerHTML = this.$t("subtotalAmount");
      headTr.appendChild(subtotalTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("totalAmount");
      headTr.appendChild(totalTh);

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let idTd = document.createElement("td");
        idTd.innerHTML = element.id;
        bodyTr.appendChild(idTd);

        let sellerNameTd = document.createElement("td");
        sellerNameTd.innerHTML = element.sellerName;
        bodyTr.appendChild(sellerNameTd);

        let invoiceTd = document.createElement("td");
        invoiceTd.innerHTML = element.sellerInvoiceNumber;
        bodyTr.appendChild(invoiceTd);

        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getTaxValue(
            element.taxes,
            tax.settingsAlias
          )} €`;
          bodyTr.appendChild(taxTd);
        }
        let subtotalTd = document.createElement("td");
        subtotalTd.innerHTML = `${element.subTotalAmount} €`;
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.totalAmount} €`;
        bodyTr.appendChild(subtotalTd);
        bodyTr.appendChild(totalTd);
        tbody.appendChild(bodyTr);
      }

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);

      return table;
    },
  },
};
