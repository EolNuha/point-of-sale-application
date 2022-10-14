<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen px-4">
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getSales`"
      :chartData="$store.state.analyticsModule.sales"
      :titleContent="`Sales`"
      :textContent="`Total day revenue of sales`"
    >
    </AreaChartMoney>
    <AreaChartSpecificDate
      :dispatchModule="`analyticsModule/getSaleStats`"
      :id="selectedProduct.id"
      :chartData="$store.state.analyticsModule.sale"
      :titleContent="`Sales on`"
      :textContent="`Revenue made`"
    >
    </AreaChartSpecificDate>
  </div>
</template>
<script>
import AreaChartMoney from "@/components/analytics/AreaChartMoney.vue";
import AreaChartSpecificDate from "@/components/analytics/AreaChartSpecificDate.vue";
export default {
  components: {
    AreaChartMoney,
    AreaChartSpecificDate,
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
