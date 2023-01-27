<template>
  <div class="main-div">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        class="bg-white dark:bg-neutral-900 p-5 rounded relative"
        id="dashboard-step-0"
      >
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("products") }}
        </h3>
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          v-if="$can('read', 'products')"
          :to="{ name: 'products' }"
          >{{ $t("productList") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          v-if="$can('write', 'products')"
          :to="{ name: 'new-product' }"
          >{{ $t("createProduct") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          v-if="$can('read', 'analytics')"
          :to="{ name: 'product-analytics' }"
          >{{ $t("productAnalytics") }}</router-link
        >
        <IconC
          iconName="TagIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px] text-theme-400"
        />
      </div>
      <div class="bg-white dark:bg-neutral-900 p-5 rounded relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("sales") }}
        </h3>
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'sales' }"
          v-if="$can('read', 'sales')"
          >{{ $t("salesList") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'new-sale' }"
          v-if="$can('write', 'sales')"
          >{{ $t("createSale") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'sale-analytics' }"
          v-if="$can('read', 'analytics')"
          >{{ $t("saleAnalytics") }}</router-link
        >
        <IconC
          iconName="ShoppingCartIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-theme-400"
        />
      </div>
      <div
        class="bg-white dark:bg-neutral-900 p-5 rounded relative"
        id="dashboard-step-1"
      >
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("purchases") }}
        </h3>
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'purchases' }"
          v-if="$can('read', 'purchases')"
          >{{ $t("purchasesList") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'new-purchase' }"
          v-if="$can('write', 'purchases')"
          >{{ $t("createPurchase") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'purchase-analytics' }"
          v-if="$can('read', 'analytics')"
          >{{ $t("purchaseAnalytics") }}</router-link
        >
        <IconC
          iconName="BuildingStorefrontIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-theme-400"
        />
      </div>
      <div class="bg-white dark:bg-neutral-900 p-5 rounded relative">
        <div
          v-if="
            !$can('read', 'users') &&
            !$can('write', 'users') &&
            !$can('read', 'analytics')
          "
          class="min-h-[50px] absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center opacity-90 bg-neutral-100 dark:bg-neutral-900 text-gray-700 dark:text-gray-200"
        >
          <IconC iconName="LockClosedIcon" iconClass="w-16 h-16" />
        </div>
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">
          {{ $t("users") }}
        </h3>
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'users' }"
          v-if="$can('read', 'users')"
          >{{ $t("usersList") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'new-user' }"
          v-if="$can('write', 'users')"
          >{{ $t("createUser") }}</router-link
        >
        <router-link
          class="text-theme-500 hover:text-theme-400 block mb-2"
          :to="{ name: 'user-analytics' }"
          v-if="$can('read', 'analytics')"
          >{{ $t("userAnalytics") }}</router-link
        >
        <IconC
          iconName="UserGroupIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-theme-400"
        />
      </div>
    </div>
    <div
      class="bg-white dark:bg-neutral-900 rounded my-5 py-8 relative px-5"
      id="dashboard-step-2"
    >
      <div
        v-if="!$can('read', 'analytics')"
        class="min-h-[400px] rounded absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center opacity-90 bg-neutral-100 dark:bg-neutral-900 text-gray-700 dark:text-gray-200"
      >
        <IconC iconName="LockClosedIcon" iconClass="w-16 h-16" />
        {{ $t("noPermissionText") }}
      </div>
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
            {{
              roundTo2(
                $store.state.analyticsModule.sales.info.currTotal
              ).toFixed(2)
            }}€
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
        class="flex flex-row items-center justify-end text-theme-500 hover:text-theme-600 uppercase text-sm"
        :to="{ name: 'sale-analytics' }"
        >{{ $t("salesReport") }}
        <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4"
      /></router-link>
    </div>
    <div class="bg-white dark:bg-neutral-900 rounded py-8 relative px-5">
      <div
        v-if="!$can('read', 'analytics')"
        class="min-h-[400px] rounded absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center opacity-90 bg-neutral-100 dark:bg-neutral-900 text-gray-700 dark:text-gray-200"
      >
        <IconC iconName="LockClosedIcon" iconClass="w-16 h-16" />
        {{ $t("noPermissionText") }}
      </div>
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
            {{
              roundTo2(
                $store.state.analyticsModule.purchases.info.currTotal
              ).toFixed(2)
            }}€
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
        class="flex flex-row items-center justify-end text-theme-500 hover:text-theme-600 uppercase text-sm"
        :to="{ name: 'purchase-analytics' }"
        >{{ $t("purchasesReport") }}
        <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4"
      /></router-link>
    </div>
  </div>
</template>

<script>
import AreaChart from "@/components/AreaChart.vue";
export default {
  components: { AreaChart },
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
    roundTo2() {
      return (num) => Math.round((Number(num) + Number.EPSILON) * 100) / 100;
    },
  },
};
</script>
