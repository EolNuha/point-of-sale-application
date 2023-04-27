<template>
  <div class="main-div">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2"></div>
      <div class="flex flex-row items-center gap-2">
        <button
          class="red-gradient-btn inline-flex items-center text-center"
          @click="download"
          type="button"
        >
          <div class="inline-flex flex-row" role="status" v-if="isPdfLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-5 h-5 text-gray-200 animate-spin fill-white"
            />
            {{ $t("downloading") }}...
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else class="inline-flex flex-row">
            <IconC
              iconType="custom"
              iconName="SolidPdfIcon"
              iconClass="w-5 h-5 fill-white mr-2"
            />
            {{ $t("download") }} PDF
          </div>
        </button>
        <button
          class="theme-gradient-btn inline-flex items-center text-center"
          @click="getPrintPdf"
          :disabled="isLoading"
          type="button"
        >
          <div class="inline-flex flex-row">
            <IconC
              iconType="solid"
              iconName="PrinterIcon"
              iconClass="w-5 h-5 fill-white mr-2"
            />
            {{ $t("print") }}
          </div>
        </button>
      </div>
    </div>
    <div
      class="bg-white dark:bg-neutral-900 rounded relative my-5 px-10 py-8 flex flex-col"
    >
      <OverlayC v-if="isLoading" />
      <div id="content">
        <div class="flex items-center flex-row justify-between">
          <h2 class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold">
            {{ $t("sale") }} #{{ $route.params.saleId }}
          </h2>
          <p class="text-gray-700 dark:text-gray-300 mr-3">
            {{ $t("date") }}: {{ sale.dateCreated?.substring(0, 10) }}
          </p>
        </div>
        <div class="overflow-x-auto sm:rounded my-5 scrollbar-style">
          <table
            class="w-full text-sm text-left text-gray-700 dark:text-gray-400 my-5"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400"
            >
              <tr>
                <th scope="col" class="py-3 px-6">{{ $t("productName") }}</th>
                <th scope="col" class="py-3 px-6">{{ $t("barcode") }}</th>
                <th scope="col" class="py-3 px-6">{{ $t("measure") }}</th>
                <th scope="col" class="py-3 px-6">{{ $t("quantity") }}</th>
                <th scope="col" class="py-3 px-6">{{ $t("price") }}</th>
                <th scope="col" class="py-3 px-6">{{ $t("tax") }}</th>
                <th scope="col" class="py-3 px-6 text-right">
                  {{ $t("total") }}
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-for="item in sale.saleItems" :key="item.id">
                <tr class="bg-white dark:bg-neutral-900">
                  <td class="py-3 px-6">
                    {{ item.product.name }}
                  </td>
                  <td class="py-3 px-6">{{ item.product.barcode }}</td>
                  <td class="py-3 px-6">{{ item.product.measure }}</td>
                  <td class="py-3 px-6">
                    <div>x {{ item.quantity }}</div>
                  </td>
                  <td class="py-3 px-6">{{ item.product.sellingPrice }} €</td>
                  <td class="py-3 px-6">
                    {{ item.taxAmount }} € ({{ item.product.tax }}%)
                  </td>
                  <td class="py-3 px-6 text-right">
                    {{
                      roundTo2(
                        item.product.sellingPrice * item.quantity
                      ).toFixed(2)
                    }}
                    €
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
          <hr class="border-gray-300 dark:border-gray-600" />
        </div>
        <div class="flex flex-row justify-end p-5">
          <div class="basis-3/4 md:basis-1/2 lg:basis-1/3">
            <table class="text-gray-700 dark:text-gray-300 w-full">
              <tbody>
                <tr>
                  <td class="py-2 uppercase">{{ $t("customerAmount") }}</td>
                  <td class="text-right py-2">{{ sale.customerAmount }} €</td>
                </tr>
                <tr>
                  <td class="py-2 uppercase">{{ $t("subTotal") }}</td>
                  <td class="text-right py-2">{{ sale.subTotalAmount }} €</td>
                </tr>
                <tr v-for="item in taxes" :key="item.settingsValue">
                  <td class="py-2 uppercase">
                    {{ $t("tax") }} ({{ item.settingsValue }}%)
                  </td>
                  <td class="text-right py-2">
                    {{
                      sale.taxes
                        ? sale.taxes[item.settingsAlias]?.taxValue || "0.00"
                        : "0.00"
                    }}
                    €
                  </td>
                </tr>
                <tr class="font-bold text-xl">
                  <td class="py-2 uppercase">{{ $t("total") }}</td>
                  <td class="text-right py-2">{{ sale.totalAmount }} €</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div
      id="printModal"
      tabindex="-1"
      aria-hidden="true"
      class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 p-4 w-full md:inset-0 h-modal md:h-full"
    >
      <div class="relative w-full max-w-7xl h-full md:h-auto">
        <div class="relative bg-white rounded shadow dark:bg-neutral-700">
          <div
            class="text-gray-700 dark:text-gray-200 flex justify-between items-center p-4 rounded-t border-b dark:border-gray-600"
          >
            <h3 class="text-xl font-semibold">
              {{ $t("printDoc", { value: $t("sale").toLowerCase() }) }}
            </h3>
            <button
              type="button"
              class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-800/50"
              @click="$hideModal('printModal')"
            >
              <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
              <span class="sr-only">Close modal</span>
            </button>
          </div>
          <iframe id="iframe" width="100%" style="height: 80vh"></iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from "jspdf";
export default {
  data() {
    return {
      isLoading: true,
      isPdfLoading: false,
      isUpdateLoading: false,
      deletedItems: [],
    };
  },
  computed: {
    sale() {
      return this.$store.state.saleModule.sale;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
    roundTo2() {
      return (num) => Math.round((Number(num) + Number.EPSILON) * 100) / 100;
    },
    getProductsTotal() {
      const products = this.sale.saleItems;
      const sum = products?.reduce((accumulator, object) => {
        return (
          this.roundTo2(accumulator) +
          this.roundTo2(object.product.sellingPrice) *
            this.roundTo2(object.quantity)
        );
      }, 0);
      return this.roundTo2(sum).toFixed(2);
    },
    getTotalWithoutTax() {
      const products = this.sale.saleItems;
      const sum = products?.reduce((accumulator, object) => {
        return (
          this.roundTo2(accumulator) +
          this.roundTo2(object.priceWithoutTax) * this.roundTo2(object.quantity)
        );
      }, 0);
      return this.roundTo2(sum).toFixed(2);
    },
  },
  async created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.$store
      .dispatch("saleModule/getSaleDetails", this.$route.params.saleId)
      .then(() => {
        this.isLoading = false;
        document.title = `${this.$t("sale")} #${this.sale.id}`;
      });
  },
  methods: {
    removeClass(element, className) {
      element.classList.remove(...className);
      const children = element.children;
      for (const child of children) {
        this.removeClass(child, className);
      }
    },
    async getPrintPdf() {
      let doc = new jsPDF();
      let elementHTML = document.getElementById("content");
      let copiedElement = elementHTML.cloneNode(true);
      this.removeClass(copiedElement, [
        "dark:bg-neutral-700",
        "dark:bg-neutral-900",
        "dark:text-gray-300",
        "dark:text-gray-400",
        "dark:border-gray-600",
      ]);
      await doc.html(copiedElement, {
        margin: [10, 10, 10, 10],
        autoPaging: "text",
        x: 0,
        y: 0,
        width: 190,
        windowWidth: 800,
      });
      let iframe = document.getElementById("iframe");
      iframe.src = doc.output("datauristring");
      this.$openModal("printModal");
    },
    async download() {
      this.isPdfLoading = true;
      const saleTxt = this.$t("sale").toLowerCase();
      const saleId = this.$route.params.saleId;
      let doc = new jsPDF();

      let elementHTML = document.querySelector("#content");

      await doc.html(elementHTML, {
        callback: function (doc) {
          // Save the PDF
          doc.save(`${saleTxt}-${saleId}-pdf.pdf`);
        },
        margin: [10, 10, 10, 10],
        autoPaging: "text",
        x: 0,
        y: 0,
        width: 190,
        windowWidth: 800,
      });
      this.isPdfLoading = false;
    },
  },
};
</script>
