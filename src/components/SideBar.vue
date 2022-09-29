<template>
  <div
    class="bg-white dark:bg-gray-900 w-64 sidebar h-screen overflow-y-auto"
    aria-label="Sidebar"
  >
    <div class="overflow-y-auto py-4 px-3">
      <ul class="space-y-2">
        <li>
          <router-link
            :to="{ name: 'home' }"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
          >
            <IconC
              iconType="outline"
              iconName="ChartPieIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span class="ml-3">Dashboard</span>
          </router-link>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="dropdown-example"
            data-collapse-toggle="dropdown-example"
          >
            <IconC
              iconType="outline"
              iconName="ServerStackIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >Management</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="dropdown-example" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'products' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >Products</router-link
              >
            </li>
          </ul>
        </li>
        <li>
          <button
            type="button"
            class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
            aria-controls="orders-dropdown"
            data-collapse-toggle="orders-dropdown"
          >
            <IconC
              iconType="outline"
              iconName="ShoppingCartIcon"
              iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
            />
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >Orders</span
            >
            <IconC iconName="ChevronDownIcon" iconClass="w-4 h-4" />
          </button>
          <ul id="orders-dropdown" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'orders' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >Orders</router-link
              >
            </li>
            <li>
              <router-link
                :to="{ name: 'new-order' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >New order</router-link
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
};
</script>

<style lang="scss">
@import "/src/styles/components/_sidebar.scss";
</style>
