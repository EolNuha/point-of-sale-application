<template>
  <div
    class="bg-white dark:bg-gray-900 w-64 sidebar min-h-screen"
    aria-label="Sidebar"
  >
    <div class="overflow-y-auto py-4 px-3">
      <ul class="space-y-2">
        <li>
          <router-link
            :to="{ name: 'home' }"
            class="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-600"
          >
            <svg
              aria-hidden="true"
              class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path>
              <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path>
            </svg>
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
            <svg
              aria-hidden="true"
              class="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z"
                clip-rule="evenodd"
              ></path>
            </svg>
            <span
              class="flex-1 ml-3 text-left whitespace-nowrap"
              sidebar-toggle-item=""
              >Products</span
            >
            <svg
              sidebar-toggle-item=""
              class="w-6 h-6"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </button>
          <ul id="dropdown-example" class="hidden py-2 space-y-2">
            <li>
              <router-link
                :to="{ name: 'products-create' }"
                class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded-lg transition duration-75 group hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600"
                >Create Product</router-link
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
  props: {
    msg: String,
  },
};
</script>

<style lang="scss">
.sidebar {
  position: fixed;
  top: 60px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}
.sidebar .router-link-active {
  @apply bg-gray-200;
  @apply dark:bg-gray-700;
}
</style>
