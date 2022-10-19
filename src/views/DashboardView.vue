<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("products") }}
        </h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'products' }"
          >{{ $t("manageProducts") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-product' }"
          >{{ $t("createProduct") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'product-analytics' }"
          >{{ $t("productAnalytics") }}</router-link
        >
        <IconC
          iconName="TagIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("sales") }}
        </h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'sales' }"
          >{{ $t("manageSales") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-sale' }"
          >{{ $t("createSale") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'sale-analytics' }"
          >{{ $t("saleAnalytics") }}</router-link
        >
        <IconC
          iconName="ShoppingCartIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("purchases") }}
        </h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'purchases' }"
          >{{ $t("managePurchases") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-purchase' }"
          >{{ $t("createPurchase") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'purchase-analytics' }"
          >{{ $t("purchaseAnalytics") }}</router-link
        >
        <IconC
          iconName="BuildingStorefrontIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("users") }}
        </h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'users' }"
          >{{ $t("manageUsers") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-user' }"
          >{{ $t("createUser") }}</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'user-analytics' }"
          >{{ $t("userAnalytics") }}</router-link
        >
        <IconC
          iconName="UserGroupIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
    </div>
    <div class="bg-white dark:bg-gray-900 rounded-xl my-5 py-8 relative px-5">
      <div
        class="flex items-center justify-between px-3 flex-wrap sm:flex-nowrap gap-2"
      >
        <div>
          <h3 class="text-gray-900 dark:text-white text-3xl">
            {{ $t("sales") }}
          </h3>
          <p class="text-gray-500 dark:text-gray-400">
            {{ $t("totalDaySales") }}
          </p>
        </div>
        <div class="inline-flex items-center flex-col" v-if="!isFetchingSales">
          <h3 class="text-3xl text-gray-900 dark:text-white">
            {{ $store.state.analyticsModule.sales.info.currTotal }}€
          </h3>
          <p
            class="inline-flex items-center text-green-500"
            v-if="$store.state.analyticsModule.sales.info.percentageDiff > 0"
          >
            +{{ $store.state.analyticsModule.sales.info.percentageDiff }}%
            <IconC iconName="ArrowLongUpIcon" iconClass="w-5 h-5" />
          </p>
          <p
            class="inline-flex items-center text-gray-500"
            v-if="$store.state.analyticsModule.sales.info.percentageDiff === 0"
          >
            {{ $store.state.analyticsModule.sales.info.percentageDiff }}%
          </p>
          <p
            class="inline-flex items-center text-red-700"
            v-if="$store.state.analyticsModule.sales.info.percentageDiff < 0"
          >
            {{ $store.state.analyticsModule.sales.info.percentageDiff }}%
            <IconC iconName="ArrowLongDownIcon" iconClass="w-5 h-5" />
          </p>
        </div>
      </div>
      <div class="relative min-h-[350px] mt-5">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetchingSales" />
        <AreaChart v-if="!isFetchingSales" :chartData="sales" />
      </div>
      <router-link
        class="flex flex-row items-center justify-end text-blue-500 hover:text-blue-600 uppercase text-sm"
        :to="{ name: 'sale-analytics' }"
        >{{ $t("salesReport") }}
        <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4"
      /></router-link>
    </div>
    <div class="bg-white dark:bg-gray-900 rounded-xl py-8 relative px-5">
      <div
        class="flex items-center justify-between px-3 flex-wrap sm:flex-nowrap gap-2"
      >
        <div>
          <h3 class="text-gray-900 dark:text-white text-3xl">
            {{ $t("purchases") }}
          </h3>
          <p class="text-gray-500 dark:text-gray-400">
            {{ $t("totalDayPurchases") }}
          </p>
        </div>
        <div
          class="inline-flex items-center flex-col"
          v-if="!isFetchingPurchases"
        >
          <h3 class="text-3xl text-gray-900 dark:text-white">
            {{ $store.state.analyticsModule.purchases.info.currTotal }}€
          </h3>
          <p
            class="inline-flex items-center text-green-500"
            v-if="
              $store.state.analyticsModule.purchases.info.percentageDiff > 0
            "
          >
            +{{
              $store.state.analyticsModule.purchases.info.percentageDiff
            }}%<IconC iconName="ArrowLongUpIcon" iconClass="w-5 h-5" />
          </p>
          <p
            class="inline-flex items-center text-gray-500"
            v-if="
              $store.state.analyticsModule.purchases.info.percentageDiff === 0
            "
          >
            {{ $store.state.analyticsModule.purchases.info.percentageDiff }}%
          </p>
          <p
            class="inline-flex items-center text-red-700"
            v-if="
              $store.state.analyticsModule.purchases.info.percentageDiff < 0
            "
          >
            {{ $store.state.analyticsModule.purchases.info.percentageDiff }}%
            <IconC iconName="ArrowLongDownIcon" iconClass="w-5 h-5" />
          </p>
        </div>
      </div>
      <div class="relative min-h-[350px]">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetchingPurchases" />
        <AreaChart v-if="!isFetchingPurchases" :chartData="purchases" />
      </div>
      <router-link
        class="flex flex-row items-center justify-end text-blue-500 hover:text-blue-600 uppercase text-sm"
        :to="{ name: 'purchase-analytics' }"
        >{{ $t("purchasesReport") }}
        <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4"
      /></router-link>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
export default {
  data() {
    return {
      isFetchingSales: true,
      isFetchingPurchases: true,
    };
  },
  watch: {
    "$i18n.locale": {
      async handler() {
        this.isFetchingSales = true;
        this.isFetchingPurchases = true;
        await setTimeout(() => {}, 100);
        this.isFetchingSales = false;
        this.isFetchingPurchases = false;
      },
    },
  },
  async created() {
    const date = new Date();
    date.setDate(date.getDate() - 6);
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
    this.$store.dispatch("analyticsModule/getSales", data).then(() => {
      this.isFetchingSales = false;
    });
    this.$store.dispatch("analyticsModule/getPurchases", data).then(() => {
      this.isFetchingPurchases = false;
    });
  },
  computed: {
    sales() {
      return this.$store.state.analyticsModule.sales;
    },
    purchases() {
      return this.$store.state.analyticsModule.purchases;
    },
  },
};
</script>
