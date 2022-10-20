<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen px-4">
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getPurchases`"
      :chartData="$store.state.analyticsModule.purchases"
      :titleContent="$t('purchases')"
      :textContent="$t('totalDayPurchaseSpendings')"
    >
    </AreaChartMoney>
    <AreaChartSpecificDate
      :dispatchModule="`analyticsModule/getPurchaseStats`"
      :chartData="$store.state.analyticsModule.purchase"
      :titleContent="`${$t('purchases')} ${$t('on')}`"
      :textContent="$t('purchasesMade')"
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
