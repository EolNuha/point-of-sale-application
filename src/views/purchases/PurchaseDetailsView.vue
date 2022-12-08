<template>
  <div class="flex flex-col bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <Form v-slot="{ errors }" @submit="updatePurchase">
      <div
        class="flex items-center justify-between flex-wrap gap-2"
        v-if="!edit"
      >
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
        class="bg-white dark:bg-neutral-900 rounded my-5 py-8 relative px-10"
      >
        <OverlayC v-if="isLoading" />
        <div id="content">
          <div class="flex items-center flex-row justify-between">
            <h2
              class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold"
            >
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
                class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="py-3 px-3">{{ $t("productName") }}</th>
                  <th scope="col" class="py-3 px-3">{{ $t("barcode") }}</th>
                  <th scope="col" class="py-3 px-3">{{ $t("stock") }}</th>
                  <th scope="col" class="py-3 px-3">
                    {{ $t("purchasedPrice") }}
                  </th>
                  <!-- <th scope="col" class="py-3 px-3">{{ $t("priceWithoutTax") }}</th> -->
                  <th scope="col" class="py-3 px-3">
                    {{ $t("sellingPrice") }}
                  </th>
                  <th scope="col" class="py-3 px-3">{{ $t("tax") }}</th>
                  <th scope="col" class="py-3 px-3 text-right">
                    {{ $t("total") }}
                  </th>
                  <th
                    scope="col"
                    class="py-3 px-3"
                    v-if="edit && purchase.purchaseItems?.length > 1"
                  ></th>
                </tr>
              </thead>
              <tbody>
                <template
                  v-for="(item, index) in purchase.purchaseItems"
                  :key="item.id"
                >
                  <tr class="bg-white dark:bg-neutral-900">
                    <td class="py-3 px-3">
                      {{ item.product.name }}
                    </td>
                    <td class="py-3 px-3">{{ item.product.barcode }}</td>
                    <td class="py-3 px-3">
                      <div v-if="edit">
                        <Field
                          required
                          :rules="isRequired"
                          :name="`${item.id}-stock`"
                          :class="
                            errors[`${item.id}-stock`]
                              ? 'ring-2 ring-red-500'
                              : ''
                          "
                          type="number"
                          step="0.01"
                          min="0.01"
                          class="default-input max-w-[100px]"
                          v-model="item.product.stock"
                        />
                      </div>
                      <div v-else>x {{ item.product.stock }}</div>
                    </td>
                    <td class="py-3 px-3">
                      <div v-if="edit">
                        <Field
                          required
                          :rules="isRequired"
                          :name="`${item.id}-purchasedPrice`"
                          :class="
                            errors[`${item.id}-purchasedPrice`]
                              ? 'ring-2 ring-red-500'
                              : ''
                          "
                          type="number"
                          step="0.01"
                          min="0.01"
                          class="default-input max-w-[100px]"
                          v-model="item.product.purchasedPrice"
                        />
                      </div>
                      <div v-else>{{ item.product.purchasedPrice }} €</div>
                    </td>
                    <!-- <td class="py-3 px-3">{{ item.priceWithoutTax }} €</td> -->
                    <td class="py-3 px-3">
                      <div v-if="edit">
                        <Field
                          required
                          :rules="isRequired"
                          :name="`${item.id}-sellingPrice`"
                          :class="
                            errors[`${item.id}-sellingPrice`]
                              ? 'ring-2 ring-red-500'
                              : ''
                          "
                          type="number"
                          step="0.01"
                          min="0.01"
                          class="default-input max-w-[100px]"
                          v-model="item.product.sellingPrice"
                        />
                      </div>
                      <div v-else>{{ item.product.sellingPrice }} €</div>
                    </td>
                    <td class="py-3 px-3">
                      {{
                        roundTo2(
                          (item.product.tax / 100) * item.product.purchasedPrice
                        ).toFixed(2)
                      }}
                      € ({{ item.product.tax }}%)
                    </td>
                    <td class="py-3 px-3 text-right">
                      {{
                        roundTo2(
                          item.product.purchasedPrice * item.product.stock
                        ).toFixed(2)
                      }}
                      €
                    </td>
                    <td
                      class="py-3 px-6 max-w-[60px]"
                      v-if="edit && purchase.purchaseItems?.length > 1"
                    >
                      <button
                        type="button"
                        :id="`delete-${item.id}-tooltip-btn`"
                        @click="deletePurchaseItem(index)"
                        class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-neutral-800/50"
                        @mouseover="
                          $showTooltip({
                            targetEl: `delete-${item.id}-tooltip`,
                            triggerEl: `delete-${item.id}-tooltip-btn`,
                          })
                        "
                      >
                        <IconC iconName="TrashIcon" iconClass="w-5 h-5" />
                        <div
                          :id="`delete-${item.id}-tooltip`"
                          role="tooltip"
                          class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                        >
                          {{ $t("delete") }}
                        </div>
                      </button>
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
                  <tr>
                    <td class="py-2">{{ $t("subTotal") }}</td>
                    <td class="text-right py-2">{{ getTotalWithoutTax }} €</td>
                  </tr>
                  <tr v-for="item in taxes" :key="item.settingsValue">
                    <template v-if="!edit">
                      <td class="py-2 uppercase">
                        {{ $t("tax") }} ({{ item.settingsValue }}%)
                      </td>
                      <td class="text-right py-2">
                        {{ getTaxValue(purchase.taxes, item.settingsAlias) }} €
                      </td>
                    </template>
                  </tr>
                  <tr class="font-bold text-xl">
                    <td class="py-2">{{ $t("total") }}</td>
                    <td class="text-right py-2">{{ getProductsTotal }} €</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <button
        class="theme-gradient-btn w-32 flex justify-center items-center"
        type="submit"
        v-if="edit"
      >
        <div role="status" v-if="isUpdateLoading">
          <IconC
            iconType="custom"
            iconName="SpinnerIcon"
            iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
          />
          <span class="sr-only">Loading...</span>
        </div>
        <div v-else>{{ $t("update") }}</div>
      </button>
      <div
        id="printModal"
        tabindex="-1"
        aria-hidden="true"
        class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 p-4 w-full md:inset-0 h-modal md:h-full"
      >
        <div class="relative w-full max-w-7xl h-full md:h-auto">
          <div class="relative bg-white rounded shadow dark:bg-gray-700">
            <div
              class="flex justify-between items-start p-4 rounded-t border-b dark:border-gray-600"
            >
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ $t("printDoc", { value: $t("purchase").toLowerCase() }) }}
              </h3>
              <button
                type="button"
                class="p-1.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-neutral-800/50"
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
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";
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
  components: {
    Field,
    Form,
  },
  props: {
    edit: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    purchase() {
      return this.$store.state.purchaseModule.purchase;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
    roundTo2() {
      return (num) => Math.round((Number(num) + Number.EPSILON) * 100) / 100;
    },
    getProductsTotal() {
      const products = this.purchase.purchaseItems;
      const sum = products?.reduce((accumulator, object) => {
        return (
          this.roundTo2(accumulator) +
          this.roundTo2(object.product.purchasedPrice) *
            this.roundTo2(object.product.stock)
        );
      }, 0);
      return this.roundTo2(sum).toFixed(2);
    },
    getTotalWithoutTax() {
      const products = this.purchase.purchaseItems;
      const sum = products?.reduce((accumulator, object) => {
        const tax_amount =
          (object.product.tax / 100) * object.product.purchasedPrice;
        const price_wo_tax = this.roundTo2(
          object.product.purchasedPrice - this.roundTo2(tax_amount)
        );
        return (
          this.roundTo2(accumulator) +
          this.roundTo2(price_wo_tax * this.roundTo2(object.product.stock))
        );
      }, 0);
      return this.roundTo2(sum).toFixed(2);
    },
    getTaxValue() {
      return (arr, alias) =>
        arr?.find((x) => x.taxAlias === alias)?.taxValue || 0;
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
      });
  },
  methods: {
    isRequired(value) {
      return value > 0 ? true : this.$t("isRequired");
    },
    async getPrintPdf() {
      let doc = new jsPDF();
      let elementHTML = document.getElementById("content");
      await doc.html(elementHTML, {
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
