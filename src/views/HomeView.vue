<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="bg-white dark:bg-gray-900 rounded-3xl my-5 py-8 relative px-5">
      <h3 class="text-gray-900 dark:text-white text-3xl">Sales</h3>
      <p class="text-gray-500 dark:text-gray-400">
        Total day sales over the last seven days
      </p>
      <div class="relative min-h-[350px]">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetchingSales" />
        <LineChart
          v-if="!isFetchingSales"
          :chartData="$store.state.analyticsModule.sales"
        />
      </div>
    </div>
    <div class="bg-white dark:bg-gray-900 rounded-3xl my-5 py-8 relative px-5">
      <h3 class="text-gray-900 dark:text-white text-3xl">Purchases</h3>
      <p class="text-gray-500 dark:text-gray-400">
        Total day purchases over the last seven days
      </p>
      <div class="relative min-h-[350px]">
        <OverlayC v-if="isFetchingPurchases" />
        <LineChart
          v-if="!isFetchingPurchases"
          :chartData="$store.state.analyticsModule.purchases"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Icons from "@/components/icons/icons.json";
import { logoutUser } from "@/router/auth/index";
export default {
  name: "HomeView",
  data() {
    return {
      isLoading: false,
      activeTab: "outline",
      icons: Icons,
      isFetchingSales: true,
      isFetchingPurchases: true,
    };
  },
  async created() {
    this.$store.dispatch("userModule/getCurrentUser").catch(() => {
      logoutUser();
      this.$router.push({ name: "signin" });
    });
    const date = new Date();
    date.setDate(date.getDate() - 7);
    const startDate =
      String(date.getFullYear()).padStart(2, "0") +
      "-" +
      String(date.getMonth() + 1).padStart(2, "0") +
      "-" +
      String(date.getDate()).padStart(2, "0");
    const endDate =
      String(new Date().getFullYear()).padStart(2, "0") +
      "-" +
      String(new Date().getMonth() + 1).padStart(2, "0") +
      "-" +
      String(new Date().getDate()).padStart(2, "0");

    const data = { startDate: startDate, endDate: endDate };
    await this.$store.dispatch("analyticsModule/getSales", data).then(() => {
      this.isFetchingSales = false;
    });
    await this.$store
      .dispatch("analyticsModule/getPurchases", data)
      .then(() => {
        this.isFetchingPurchases = false;
      });
  },
};
</script>

<style>
.dark .apexcharts-text tspan {
  fill: white !important;
}
</style>
