<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">Products</h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'products' }"
          >Manage Products</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-product' }"
          >Create Product</router-link
        >
        <IconC
          iconName="TagIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">Sales</h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'sales' }"
          >Manage Sales</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-sale' }"
          >Create Sale</router-link
        >
        <IconC
          iconName="ShoppingCartIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">Purchases</h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'purchases' }"
          >Manage Purchases</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-purchase' }"
          >Create Purchase</router-link
        >
        <IconC
          iconName="BuildingStorefrontIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
      <div class="bg-white dark:bg-gray-900 p-5 rounded-xl relative">
        <h3 class="text-gray-900 dark:text-white text-2xl mb-2">Users</h3>
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'users' }"
          >Manage Users</router-link
        >
        <router-link
          class="text-blue-500 hover:text-blue-400 block mb-2"
          :to="{ name: 'new-user' }"
          >Create User</router-link
        >
        <IconC
          iconName="UserGroupIcon"
          iconClass="w-12 h-12 absolute right-[5px] bottom-[5px]  text-blue-500/50"
        />
      </div>
    </div>
    <div class="bg-white dark:bg-gray-900 rounded-xl my-5 py-8 relative px-5">
      <h3 class="text-gray-900 dark:text-white text-3xl">Sales</h3>
      <p class="text-gray-500 dark:text-gray-400">
        Total day sales over the last seven days
      </p>
      <div class="relative min-h-[350px]">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetchingSales" />
        <AreaChart
          v-if="!isFetchingSales"
          :chartData="$store.state.analyticsModule.sales"
        />
      </div>
    </div>
    <div class="bg-white dark:bg-gray-900 rounded-xl py-8 relative px-5">
      <h3 class="text-gray-900 dark:text-white text-3xl">Purchases</h3>
      <p class="text-gray-500 dark:text-gray-400">
        Total day purchases over the last seven days
      </p>
      <div class="relative min-h-[350px]">
        <OverlayC v-if="isFetchingPurchases" />
        <AreaChart
          v-if="!isFetchingPurchases"
          :chartData="$store.state.analyticsModule.purchases"
        />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { logoutUser } from "@/router/auth/index";
export default {
  data() {
    return {
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
