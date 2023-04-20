<template>
  <div
    class="flex flex-col bg-neutral-200 dark:bg-neutral-800 min-h-screen p-4"
  >
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
      class="bg-white dark:bg-neutral-900 rounded my-5 py-8 relative px-10 flex flex-col"
    >
      <OverlayC v-if="isLoading" />
      <div id="content">
        <div class="flex items-center flex-row justify-between">
          <h2 class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold">
            {{ $t("purchase") }} #{{ $route.params.purchaseId }}
          </h2>
          <p class="text-gray-700 dark:text-gray-300 mr-2">
            {{ $t("date") }}: {{ purchase.dateCreated?.substring(0, 10) }}
          </p>
        </div>
        <div class="flex flex-row pt-5">
          <div class="basis-3/4 md:basis-1/2 lg:basis-1/3">
            <table class="text-gray-700 dark:text-gray-400 text-sm w-full">
              <tbody>
                <tr>
                  <td class="py-2">{{ $t("sellerName") }}</td>
                  <td class="text-right py-2">{{ purchase.sellerName }}</td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("invoiceNumber") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.sellerInvoiceNumber }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("fiscalNumber") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.sellerFiscalNumber }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("taxNumber") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.sellerTaxNumber }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="overflow-x-auto sm:rounded my-5 scrollbar-style">
          <table
            class="w-full text-sm text-left text-gray-700 dark:text-gray-400 my-5"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400"
            >
              <tr>
                <th scope="col" class="py-3 px-3">{{ $t("productName") }}</th>
                <th scope="col" class="py-3 px-3">{{ $t("barcode") }}</th>
                <th scope="col" class="py-3 px-3">{{ $t("measure") }}</th>
                <th scope="col" class="py-3 px-3">{{ $t("stock") }}</th>
                <th scope="col" class="py-3 px-3">
                  {{ $t("purchasedPriceWOTax") }}
                </th>
                <th scope="col" class="py-3 px-3">
                  {{ $t("purchasedPrice") }}
                </th>
                <!-- <th scope="col" class="py-3 px-3">
                    {{ $t("sellingPrice") }}
                  </th> -->
                <th scope="col" class="py-3 px-3">{{ $t("tax") }}</th>
                <th scope="col" class="py-3 px-3 text-right">
                  {{ $t("total") }}
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-for="item in purchase.purchaseItems" :key="item.id">
                <tr class="bg-white dark:bg-neutral-900">
                  <td class="py-3 px-3">
                    {{ item.product.name }}
                  </td>
                  <td class="py-3 px-3">{{ item.product.barcode }}</td>
                  <td class="py-3 px-3">
                    <div>
                      {{ $t(item.product.measure) }}
                    </div>
                  </td>
                  <td class="py-3 px-3">
                    <div>x {{ item.product.stock }}</div>
                  </td>
                  <td class="py-3 px-3">
                    <div>{{ item.product.purchasedPriceWOTax }} €</div>
                  </td>
                  <td class="py-3 px-3">
                    <div>{{ item.product.purchasedPrice }} €</div>
                  </td>
                  <td class="py-3 px-3">
                    {{ item.taxAmount }}
                    € ({{ item.product.tax }}%)
                  </td>
                  <td class="py-3 px-3 text-right">
                    {{ item.totalAmount }}
                    €
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
        <hr class="border-gray-300 dark:border-gray-600" />
        <div class="flex flex-row justify-end p-5">
          <div class="basis-3/4 md:basis-1/2 lg:basis-1/3">
            <table class="text-gray-700 dark:text-gray-300 w-full">
              <tbody>
                <template v-for="item in taxes" :key="item.id">
                  <tr>
                    <td class="py-2 uppercase">
                      {{ $t("tax") }} ({{ item.settingsValue }}%)
                    </td>
                    <td class="text-right py-2">
                      {{
                        purchase.taxes
                          ? purchase.taxes[item.settingsAlias]?.taxValue ||
                            "0.00"
                          : "0.00"
                      }}
                      €
                    </td>
                  </tr>
                  <tr>
                    <td class="py-2 uppercase">
                      {{ $t("subTotal") }} ({{ item.settingsValue }}%)
                    </td>
                    <td class="text-right py-2">
                      {{
                        purchase.taxes
                          ? purchase.taxes[item.settingsAlias]
                              ?.totalWithoutTax || "0.00"
                          : "0.00"
                      }}
                      €
                    </td>
                  </tr>
                </template>
                <tr v-if="Number(purchase.rabatAmount) > 0">
                  <td class="py-2">{{ $t("rabat") }}</td>
                  <td class="text-right py-2">{{ purchase.rabatAmount }} €</td>
                </tr>
                <tr class="font-bold text-xl">
                  <td class="py-2">{{ $t("total") }}</td>
                  <td class="text-right py-2">{{ purchase.totalAmount }} €</td>
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
              {{ $t("printDoc", { value: $t("purchase").toLowerCase() }) }}
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
    };
  },
  computed: {
    purchase() {
      return this.$store.state.purchaseModule.purchase;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
  },
  async created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.$store
      .dispatch(
        "purchaseModule/getPurchaseDetails",
        this.$route.params.purchaseId
      )
      .then(() => {
        this.isLoading = false;
        document.title = `${this.$t("purchase")} #${this.purchase.id}`;
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
      const purchaseTxt = this.$t("purchase").toLowerCase();
      const purchaseId = this.$route.params.purchaseId;
      let doc = new jsPDF();

      let elementHTML = document.querySelector("#content");

      await doc.html(elementHTML, {
        callback: function (doc) {
          // Save the PDF
          doc.save(`${purchaseTxt}-${purchaseId}.pdf`, { extensions: ["pdf"] });
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
    deletePurchaseItem(index) {
      this.deletedItems.push(this.purchase.purchaseItems[index]);
      this.purchase.purchaseItems.splice(index, 1);
    },
    updatePurchase() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("purchaseModule/updatePurchase", {
          id: this.$route.params.purchaseId,
          deletedItems: this.deletedItems,
          purchaseItems: this.purchase.purchaseItems,
        })
        .then(() => {
          this.$toast.success(
            this.$t("updatedSuccessfully", {
              value: this.$t("purchase"),
            })
          );
          this.isUpdateLoading = false;
        })
        .catch(() => {
          this.$toast.error(this.$t("somethingWrong"));
          this.isUpdateLoading = false;
        });
    },
  },
};
</script>
