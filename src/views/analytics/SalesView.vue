<template>
  <div
    class="bg-neutral-200 dark:bg-neutral-800 min-h-screen p-4 flex flex-col gap-4"
  >
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
      <template #totalExtra>
        <p>
          {{ $t("gross") }}:
          {{
            Number($store.state.analyticsModule.sale.info.grossTotal).toFixed(
              2
            )
          }}€
        </p>
        <p>
          {{ $t("net") }}:
          {{
            Number($store.state.analyticsModule.sale.info.netTotal).toFixed(2)
          }}€
        </p>
      </template>
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
