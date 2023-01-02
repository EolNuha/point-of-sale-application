<template>
  <div class="bg-gray-200 dark:bg-neutral-800 min-h-screen px-4">
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getSales`"
      :chartData="$store.state.analyticsModule.sales"
      :titleContent="$t('sales')"
      :textContent="$t('totalDayRevenueSales')"
    >
    </AreaChartMoney>
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getSalesGrossProfit`"
      :chartData="$store.state.analyticsModule.salesGrossProfit"
      :titleContent="$t('grossProfit')"
      :textContent="$t('totalSalesGrossProfit')"
    >
    </AreaChartMoney>
    <AreaChartSpecificDate
      :dispatchModule="`analyticsModule/getSaleStats`"
      :chartData="$store.state.analyticsModule.sale"
      :titleContent="`${$t('sales')} ${$t('on')}`"
      :textContent="$t('revenueMade')"
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
    };
  },
};
</script>
