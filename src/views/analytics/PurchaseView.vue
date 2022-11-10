<template>
  <div class="bg-gray-200 dark:bg-neutral-800 min-h-screen px-4">
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
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getSellerStats`"
      :id="selectedSeller.sellerName"
      :chartData="$store.state.analyticsModule.sellerStats"
      :titleContent="`${$t('sellerName')}: ${selectedSeller.sellerName}`"
      :textContent="$t('purchasesMade')"
    >
      <div
        class="flex flex-row flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">{{ $t("product") }}:</span>
        <v-select
          class="w-full min-w-[150px] md:w-[200px] default-input"
          v-model="selectedSeller"
          :value="sellers"
          :options="sellers"
          :clearable="false"
          :reduce="(sellers) => sellers"
          label="sellerName"
        ></v-select>
      </div>
    </AreaChartMoney>
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
      selectedSeller: {},
    };
  },
  computed: {
    sellers() {
      return this.$store.getters["purchaseModule/getSellersList"];
    },
  },
  async created() {
    await this.$store
      .dispatch("purchaseModule/getSellers", {
        page: 1,
        per_page: 1000000000,
      })
      .then((res) => {
        this.selectedSeller = res.data.data[0];
      });
  },
};
</script>
