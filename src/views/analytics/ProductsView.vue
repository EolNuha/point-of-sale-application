<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen px-4">
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getProductsSoldbyAmount`"
      :chartData="$store.state.analyticsModule.productsSoldbyAmount"
      :titleContent="`Top 10 Products`"
      :textContent="`That made the most revenue`"
    >
    </AreaChartMoney>
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getProductStats`"
      :id="selectedProduct.id"
      :chartData="$store.state.analyticsModule.productStats"
      :titleContent="`Product: ${selectedProduct.name}`"
      :textContent="`Revenue made`"
    >
      <div
        class="flex flex-row flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">Product:</span>
        <v-select
          class="w-full min-w-[150px] md:w-[200px] default-input"
          v-model="selectedProduct"
          :value="products"
          :options="products"
          :clearable="false"
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
      currentDate: "",
      startDate: "",
      endDate: "",
      selectedProduct: {},
    };
  },
  computed: {
    products() {
      return this.$store.getters["productModule/getProductsList"];
    },
  },
  created() {
    this.$store
      .dispatch("productModule/getProducts", {
        page: 1,
        per_page: 1000000000,
      })
      .then((res) => {
        this.selectedProduct = res.data.data[0];
      });
  },
};
</script>
