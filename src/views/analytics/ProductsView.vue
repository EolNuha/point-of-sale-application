<template>
  <div
    class="bg-neutral-200 dark:bg-neutral-800 min-h-screen p-4 flex flex-col gap-4"
  >
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getProductsSoldbyAmount`"
      :chartData="$store.state.analyticsModule.productsSoldbyAmount"
      :titleContent="$t('topProducts')"
      :textContent="$t('topProductsMostRevenue')"
      :chartType="'pie'"
    >
    </AreaChartMoney>
    <div class="grid grid-cols-2 gap-4">
      <AreaChartMoney
        :dispatchModule="`analyticsModule/getProductsbyGrossProfit`"
        :chartData="$store.state.analyticsModule.productsSoldbyGrossProfit"
        :titleContent="`${$t('topProducts')} - ${$t('grossProfit')}`"
        :textContent="$t('topProductsMostGrossProfit')"
        :chartType="'pie'"
      >
      </AreaChartMoney>
      <AreaChartMoney
        :dispatchModule="`analyticsModule/getProductsbyNetProfit`"
        :chartData="$store.state.analyticsModule.productsSoldbyNetProfit"
        :titleContent="`${$t('topProducts')} - ${$t('netProfit')}`"
        :textContent="$t('topProductsMostNetProfit')"
        :chartType="'pie'"
      >
      </AreaChartMoney>
    </div>
    <AreaChartMoney
      v-if="selectedProduct"
      :dispatchModule="`analyticsModule/getProductStats`"
      :id="selectedProduct?.id"
      :chartData="$store.state.analyticsModule.productStats"
      :titleContent="`${$t('product')}: ${selectedProduct?.name}`"
      :textContent="$t('revenueMade')"
    >
      <div
        class="flex flex-row flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">{{ $t("product") }}:</span>
        <v-select
          class="w-full min-w-[150px] md:w-[200px] default-input"
          v-model="selectedProduct"
          @search="($event, loading) => searchProducts($event, loading)"
          :value="products"
          :options="products"
          :clearable="false"
          :filterable="false"
          :reduce="(products) => products"
          label="name"
        ></v-select>
      </div>
    </AreaChartMoney>
  </div>
</template>
<script>
import AreaChartMoney from "@/components/analytics/AreaChartMoney.vue";
export default {
  components: {
    AreaChartMoney,
  },
  data() {
    return {
      isFetching: true,
      startDate: "",
      endDate: "",
      selectedProduct: null,
      search: "",
    };
  },
  computed: {
    products() {
      return this.$store.getters["productModule/getProductsList"];
    },
  },
  async created() {
    this.getProducts(this.search).then(() => {
      this.selectedProduct = this.products[0];
    });
  },
  methods: {
    async searchProducts(search, loading) {
      this.search = search;
      loading(true);
      await this.getProducts(search);
      loading(false);
    },
    async getProducts(search) {
      await this.$store.dispatch("productModule/getProducts", {
        page: 1,
        per_page: 20,
        sort_column: "name",
        sort_dir: "asc",
        search: search,
      });
    },
  },
};
</script>
