<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <Form v-slot="{ errors }" @submit="updateSale">
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
        class="bg-white dark:bg-neutral-900 rounded relative my-5 px-10 py-8 flex flex-col"
      >
        <OverlayC v-if="isLoading" />
        <div id="content">
          <div class="flex items-center flex-row justify-between">
            <h2
              class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold"
            >
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
                class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400"
              >
                <tr>
                  <th scope="col" class="py-3 px-6">{{ $t("productName") }}</th>
                  <th scope="col" class="py-3 px-6">{{ $t("barcode") }}</th>
                  <th scope="col" class="py-3 px-6">{{ $t("quantity") }}</th>
                  <th scope="col" class="py-3 px-6">{{ $t("price") }}</th>
                  <th scope="col" class="py-3 px-6">{{ $t("tax") }}</th>
                  <th scope="col" class="py-3 px-6 text-right">
                    {{ $t("total") }}
                  </th>
                  <th
                    scope="col"
                    class="py-3 px-6"
                    v-if="edit && sale.saleItems?.length > 1"
                  ></th>
                </tr>
              </thead>
              <tbody>
                <template
                  v-for="(item, index) in sale.saleItems"
                  :key="item.id"
                >
                  <tr class="bg-white dark:bg-neutral-900">
                    <td class="py-3 px-6">
                      {{ item.product.name }}
                    </td>
                    <td class="py-3 px-6">{{ item.product.barcode }}</td>
                    <td class="py-3 px-6">
                      <div v-if="edit">
                        <Field
                          required
                          :rules="isRequired"
                          type="number"
                          :name="`${item.id}-product`"
                          step="0.01"
                          min="0.01"
                          class="default-input max-w-[100px]"
                          :class="
                            errors[`${item.id}-product`]
                              ? 'ring-2 ring-red-500'
                              : ''
                          "
                          v-model="item.quantity"
                        />
                      </div>
                      <div v-else>x {{ item.quantity }}</div>
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
                    <td class="py-3 px-6 max-w-[60px]" v-if="edit">
                      <button
                        :id="`delete-${item.id}-tooltip-btn`"
                        type="button"
                        @click="deleteSaleItem(index)"
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
                          class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                        >
                          {{ $t("delete") }}
                        </div>
                      </button>
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
                    <td class="text-right py-2">{{ getTotalWithoutTax }} €</td>
                  </tr>
                  <tr v-for="item in taxes" :key="item.settingsValue">
                    <template v-if="!edit">
                      <td class="py-2 uppercase">
                        {{ $t("tax") }} ({{ item.settingsValue }}%)
                      </td>
                      <td class="text-right py-2">
                        {{ getTaxValue(sale.taxes, item.settingsAlias) }} €
                      </td>
                    </template>
                  </tr>
                  <tr class="font-bold text-xl">
                    <td class="py-2 uppercase">{{ $t("total") }}</td>
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
        v-if="edit && sale.saleItems?.length > 1"
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
          <div class="relative bg-white rounded shadow dark:bg-neutral-700">
            <div
              class="flex justify-between items-start p-4 rounded-t border-b dark:border-gray-600"
            >
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ $t("printDoc", { value: $t("sale").toLowerCase() }) }}
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
    getTaxValue() {
      return (arr, alias) =>
        arr?.find((x) => x.taxAlias === alias)?.taxValue ||
        Number(0).toFixed(2);
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
    deleteSaleItem(index) {
      this.deletedItems.push(this.sale.saleItems[index]);
      this.sale.saleItems.splice(index, 1);
    },
    updateSale() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("saleModule/updateSale", {
          id: this.$route.params.saleId,
          deletedItems: this.deletedItems,
          saleItems: this.sale.saleItems,
        })
        .then(() => {
          this.$toast.success(
            this.$t("updatedSuccessfully", {
              value: this.$t("sale"),
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
