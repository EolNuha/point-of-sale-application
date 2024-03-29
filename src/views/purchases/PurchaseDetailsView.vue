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
            {{ $t("date") }}: {{ purchase.date_created?.substring(0, 10) }}
          </p>
        </div>
        <div class="flex flex-row pt-5 w-full">
          <div class="basis-3/4 md:basis-1/2 lg:basis-1/3">
            <table class="text-gray-700 dark:text-gray-400 text-sm w-full">
              <tbody>
                <tr>
                  <td class="py-2">{{ $t("seller_name") }}</td>
                  <td class="text-right py-2 tracking-jsPDF">
                    {{ purchase.seller_name }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("invoice_number") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.seller_invoice_number }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("fiscal_number") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.seller_fiscal_number }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("tax_number") }}</td>
                  <td class="text-right py-2">
                    {{ purchase.seller_tax_number || "-" }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="basis-3/4 md:basis-1/2 lg:basis-1/3 ml-auto">
            <table class="text-gray-700 dark:text-gray-400 text-sm w-full">
              <tbody>
                <tr>
                  <td class="py-2">{{ $t("buyer_name") }}</td>
                  <td class="text-right py-2 tracking-jsPDF">
                    {{ company.name }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("address") }}</td>
                  <td class="text-right py-2">
                    {{ company.address }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("fiscal_number") }}</td>
                  <td class="text-right py-2">
                    {{ company.fiscal_number }}
                  </td>
                </tr>
                <tr>
                  <td class="py-2">{{ $t("tax_number") }}</td>
                  <td class="text-right py-2">
                    {{ company.tax_number || "-" }}
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
              <tr class="tracking-jsPDF">
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("product_name") }}
                </th>
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("barcode") }}
                </th>
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("measure") }}
                </th>
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("stock") }}
                </th>
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("purchased_price_wo_tax") }}
                </th>
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("purchased_price") }}
                </th>
                <!-- <th scope="col" class="py-3 px-3">
                    {{ $t("selling_price") }}
                  </th> -->
                <th scope="col" class="py-3 px-3 whitespace-nowrap">
                  {{ $t("tax") }}
                </th>
                <th scope="col" class="py-3 px-3 text-right whitespace-nowrap">
                  {{ $t("total") }}
                </th>
              </tr>
            </thead>
            <tbody>
              <template v-for="item in purchase.purchase_items" :key="item.id">
                <tr class="bg-white dark:bg-neutral-900 tracking-jsPDF">
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
                    <div>{{ item.product.stock }}</div>
                  </td>
                  <td class="py-3 px-3">
                    <div>{{ item.product.purchased_price_wo_tax }} €</div>
                  </td>
                  <td class="py-3 px-3">
                    <div>{{ item.product.purchased_price }} €</div>
                  </td>
                  <td class="py-3 px-3">
                    {{ item.tax_amount }}
                    € ({{ item.product.tax }}%)
                  </td>
                  <td class="py-3 px-3 text-right">
                    {{ item.total_amount }}
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
              <tbody class="tracking-jsPDF">
                <template v-for="item in taxes" :key="item.id">
                  <tr class="tracking-jsPDF">
                    <td class="py-2 uppercase">
                      {{ $t("tax") }} ({{ item.settings_value }}%)
                    </td>
                    <td class="text-right py-2">
                      {{
                        purchase.taxes
                          ? purchase.taxes[item.settings_alias]?.tax_value ||
                            "0.00"
                          : "0.00"
                      }}
                      €
                    </td>
                  </tr>
                  <tr class="tracking-jsPDF">
                    <td class="py-2 uppercase">
                      {{ $t("subTotal") }} ({{ item.settings_value }}%)
                    </td>
                    <td class="text-right py-2">
                      {{
                        purchase.taxes
                          ? purchase.taxes[item.settings_alias]
                              ?.total_without_tax || "0.00"
                          : "0.00"
                      }}
                      €
                    </td>
                  </tr>
                </template>
                <tr v-if="Number(purchase.rabat_amount) > 0">
                  <td class="py-2">{{ $t("rabat") }}</td>
                  <td class="text-right py-2">{{ purchase.rabat_amount }} €</td>
                </tr>
                <tr class="font-bold text-xl">
                  <td class="py-2">{{ $t("total") }}</td>
                  <td class="text-right py-2">{{ purchase.total_amount }} €</td>
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
    company() {
      return this.$store.state.settingsModule.company;
    },
    purchase() {
      return this.$store.state.purchaseModule.purchase;
    },
    taxes() {
      return this.$store.state.settingsModule.settings_type.tax?.filter(
        (item) => item.settings_alias !== "zero"
      );
    },
  },
  async created() {
    await this.$store.dispatch("settingsModule/getCompany");
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
    async createPdf(elementHTML, options) {
      let doc = new jsPDF();
      let copiedElement = elementHTML.cloneNode(true);
      this.removeClass(copiedElement, [
        "dark:bg-neutral-700",
        "dark:bg-neutral-800",
        "dark:bg-neutral-900",
        "dark:text-gray-200",
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
        windowWidth: 1000, // Spread operator to use the provided options
        // eslint-disable-next-line no-unused-vars
        callback: options.callback || function (doc) {}, // Default callback if not provided
      });
      return doc;
    },

    async getPdf() {
      let elementHTML = document.getElementById("content");
      return this.createPdf(elementHTML, {});
    },

    async getPrintPdf() {
      const doc = await this.getPdf();
      let iframe = document.getElementById("iframe");
      iframe.src = doc.output("datauristring");
      this.$openModal("printModal");
    },

    async download() {
      this.isPdfLoading = true;
      const purchaseTxt = this.$t("purchase").toLowerCase();
      const purchaseId = this.$route.params.purchaseId;
      let elementHTML = document.querySelector("#content");

      await this.createPdf(elementHTML, {
        callback: function (doc) {
          doc.save(`${purchaseTxt}-${purchaseId}.pdf`, { extensions: ["pdf"] });
        },
      });
      this.isPdfLoading = false;
    },
    deletePurchaseItem(index) {
      this.deletedItems.push(this.purchase.purchase_items[index]);
      this.purchase.purchase_items.splice(index, 1);
    },
    updatePurchase() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("purchaseModule/updatePurchase", {
          id: this.$route.params.purchaseId,
          deletedItems: this.deletedItems,
          purchase_items: this.purchase.purchase_items,
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
