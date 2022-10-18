<template>
  <div
    class="bg-white dark:bg-gray-900 w-64 sidebar overflow-y-auto overflow-x-hidden duration-300 scrollbar-style"
    id="sidebar"
    aria-label="Sidebar"
  >
    <div class="overflow-y-auto overflow-x-hidden py-4 px-3">
      <ul class="space-y-2">
        <li>
          <router-link
            :to="{ name: 'dashboard' }"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
          >
            <IconC
              iconType="outline"
              iconName="ChartPieIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span class="ml-3">{{ $t("dashboard") }}</span>
          </router-link>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="products-sidebar"
            data-collapse-toggle="products-sidebar"
          >
            <IconC
              iconType="outline"
              iconName="TagIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >{{ $t("products") }}</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="products-sidebar" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'new-product' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("newProduct") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'products' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("productList") }}</router-link
              >
            </li>
          </ul>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="sales-dropdown"
            data-collapse-toggle="sales-dropdown"
          >
            <IconC
              iconType="outline"
              iconName="ShoppingCartIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >{{ $t("sales") }}</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="sales-dropdown" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'new-sale' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("newSale") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'sales' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("salesList") }}</router-link
              >
            </li>
          </ul>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="purchases-sidebar"
            data-collapse-toggle="purchases-sidebar"
          >
            <IconC
              iconType="outline"
              iconName="BuildingStorefrontIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >{{ $t("purchases") }}</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="purchases-sidebar" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'new-purchase' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("newPurchase") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'purchases' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("purchasesList") }}</router-link
              >
            </li>
          </ul>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="users-sidebar-dropdown"
            data-collapse-toggle="users-sidebar-dropdown"
          >
            <IconC
              iconType="outline"
              iconName="UserGroupIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >{{ $t("users") }}</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="users-sidebar-dropdown" class="hidden py-2 space-y-2">
            <li v-if="user.userType === 'admin'">
              <router-link
                :to="{ name: 'new-user' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("newUser") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'users' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("usersList") }}</router-link
              >
            </li>
          </ul>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="analytics-sidebar-dropdown"
            data-collapse-toggle="analytics-sidebar-dropdown"
          >
            <IconC
              iconType="outline"
              iconName="ArrowTrendingUpIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >{{ $t("analytics") }}</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="analytics-sidebar-dropdown" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'product-analytics' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("products") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'sale-analytics' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("sales") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'purchase-analytics' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("purchases") }}</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'user-analytics' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >{{ $t("users") }}</router-link
              >
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "SideBar",
  computed: {
    user() {
      return this.$store.state.userModule.currentUser;
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_sidebar.scss";
</style>
