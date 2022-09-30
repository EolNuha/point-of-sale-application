<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center w-1/2">
        <label for="simple-search" class="sr-only">Search</label>
        <div class="relative w-full">
          <div
            class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none"
          >
            <IconC
              iconType="solid"
              iconName="MagnifyingGlassIcon"
              iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
            />
          </div>
          <input
            @input="
              debounce(() => {
                searchQuery = $event.target.value;
              })
            "
            type="text"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search"
          />
        </div>
      </div>
      <button
        @click="
          $router.push({
            name: 'new-purchase',
          })
        "
        class="blue-gradient-btn flex items-center text-center"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        New Purchase
      </button>
    </div>

    <div
      class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style min-h-65"
    >
      <table
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <OverlayC v-if="isTableLoading" />
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Total Amount</th>
            <th scope="col" class="py-3 px-6">Seller Name</th>
            <th scope="col" class="py-3 px-6">Seller Invoice Number</th>
            <th scope="col" class="py-3 px-6"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="purchase in purchases" :key="purchase.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <th
                scope="row"
                class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
              >
                {{ purchase.id }}
              </th>
              <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
              <td class="py-2 px-6">{{ purchase.sellerName }}</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ purchase.sellerInvoiceNumber }}
              </td>
              <td class="py-2 px-6">
                <button
                  class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                >
                  <IconC
                    iconName="DocumentMagnifyingGlassIcon"
                    iconClass="h-5 w-5 text-gray-900 dark:text-gray-300"
                  />
                </button>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getPurchases($event)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isTableLoading: false,
      currentPage: 1,
      searchQuery: "",
    };
  },
  setup() {
    function createDebounce() {
      let timeout = null;
      return function (func, delayMs) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          func();
        }, delayMs || 500);
      };
    }

    return {
      debounce: createDebounce(),
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("purchaseModule/getPurchases", {
            page: this.currentPage,
            search: value,
          });
          this.isTableLoading = false;
        } catch {
          this.isTableLoading = false;
        }
      },
    },
  },
  created() {
    this.reload();
  },
  computed: {
    purchases() {
      return this.$store.getters["purchaseModule/getPurchasesList"];
    },
    pagination() {
      return this.$store.getters["purchaseModule/getPurchasesPagination"];
    },
  },
  methods: {
    reload() {
      this.isTableLoading = true;
      this.selectedProduct = {};
      this.$store
        .dispatch("purchaseModule/getPurchases", {
          page: this.currentPage,
        })
        .then(() => {
          this.isTableLoading = false;
        })
        .catch(() => {
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    getPurchases(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("purchaseModule/getPurchases", { page: page })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
  },
};
</script>
