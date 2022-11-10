<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2"></div>
      <div class="flex flex-row items-center gap-2">
        <button class="red-gradient-btn inline-flex items-center text-center">
          <div class="inline-flex flex-row" role="status" v-if="isPdfLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-5 h-5 text-gray-200 animate-spin fill-white"
            />
            Downloading...
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else class="inline-flex flex-row">
            <IconC
              iconType="custom"
              iconName="SolidPdfIcon"
              iconClass="w-5 h-5 fill-white mr-2"
            />
            Download PDF
          </div>
        </button>
      </div>
    </div>
    <div
      class="bg-white dark:bg-neutral-900 rounded-3xl my-5 py-8 relative px-10"
    >
      <OverlayC v-if="isLoading" />
      <div class="flex items-center flex-row justify-between">
        <h2 class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold">
          {{ $t("sale") }} #{{ $route.params.saleId }}
        </h2>
        <p class="text-gray-700 dark:text-gray-300">
          {{ $t("date") }}: {{ sale.dateCreated.substring(0, 10) }}
        </p>
      </div>
      <div class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style">
        <table
          class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative my-5"
        >
          <thead
            class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400"
          >
            <tr>
              <th scope="col" class="py-3 px-6">ID</th>
              <th scope="col" class="py-3 px-6">{{ $t("productName") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("barcode") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("quantity") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("price") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("priceWithoutTax") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("tax") }}</th>
              <th scope="col" class="py-3 px-6">{{ $t("total") }}</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in sale.saleItems" :key="item.id">
              <tr class="bg-white dark:bg-neutral-900">
                <td class="py-3 px-6">{{ item.product.id }}</td>
                <td class="py-3 px-6">
                  {{ item.product.name }}
                </td>
                <td class="py-3 px-6">{{ item.product.barcode }}</td>
                <td class="py-3 px-6">x {{ item.quantity }}</td>
                <td class="py-3 px-6 max-w-xs">
                  {{ item.product.sellingPrice }} €
                </td>
                <td class="py-3 px-6 max-w-xs">{{ item.priceWithoutTax }} €</td>
                <td class="py-3 px-6 max-w-xs">
                  {{ item.taxAmount }} € ({{ item.product.tax }}%)
                </td>
                <td class="py-3 px-6 max-w-xs">
                  {{ (item.product.sellingPrice * item.quantity).toFixed(2) }} €
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <hr class="border-gray-500" />
      </div>
      <div class="flex flex-row justify-end p-5">
        <div class="basis-3/4 md:basis-1/2 lg:basis-1/4">
          <table class="text-gray-700 dark:text-gray-300 w-full">
            <tbody>
              <tr>
                <td class="py-2 uppercase">{{ $t("subTotal") }}</td>
                <td class="text-right py-2">{{ sale.subTotalAmount }} €</td>
              </tr>
              <tr v-for="item in taxes" :key="item.settingsValue">
                <td class="py-2 uppercase">
                  {{ $t("tax") }} ({{ item.settingsValue }}%)
                </td>
                <td class="text-right py-2">
                  {{ getTaxValue(sale.taxes, item.settingsAlias) }} €
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
</template>

<script>
export default {
  data() {
    return {
      isLoading: true,
      isPdfLoading: false,
    };
  },
  computed: {
    sale() {
      return this.$store.state.saleModule.sale;
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
      .dispatch("saleModule/getSaleDetails", this.$route.params.saleId)
      .then(() => {
        this.isLoading = false;
      });
  },
  methods: {
    getTaxValue(arr, alias) {
      return arr.find((x) => x.taxAlias === alias)?.taxValue || 0;
    },
  },
};
</script>
