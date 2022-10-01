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
              $debounce(() => {
                searchQuery = $event.target.value;
              })
            "
            type="text"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search"
          />
        </div>
      </div>
      <button
        @click="
          $router.push({
            name: 'new-sale',
          })
        "
        class="blue-gradient-btn flex items-center text-center"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        New Sale
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
            <th scope="col" class="py-3 px-6">Customer Amount</th>
            <th scope="col" class="py-3 px-6">Change Amount</th>
            <th scope="col" class="py-3 px-6"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="sale in sales" :key="sale.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <th
                scope="row"
                class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
              >
                {{ sale.id }}
              </th>
              <td class="py-2 px-6">{{ sale.totalAmount }} €</td>
              <td class="py-2 px-6">{{ sale.customerAmount }} €</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ sale.changeAmount }} €
              </td>
              <td class="py-2 px-6">
                <button
                  @click="
                    $router.push({
                      name: 'sale-view',
                      params: { saleId: sale.id },
                    })
                  "
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
      @pageChange="getSales($event)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isTableLoading: false,
      selectedProduct: {},
      selectedProductToDelete: {},
      currentPage: 1,
      searchQuery: "",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("saleModule/getSales", {
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
  computed: {
    sales() {
      return this.$store.getters["saleModule/getSalesList"];
    },
    pagination() {
      return this.$store.getters["saleModule/getSalesPagination"];
    },
  },
  created() {
    this.reload();
  },
  methods: {
    reload() {
      this.isTableLoading = true;
      this.selectedProduct = {};
      this.$store
        .dispatch("saleModule/getSales", {
          page: this.currentPage,
        })
        .then(() => {
          this.isTableLoading = false;
        })
        .catch(() => {
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    getSales(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("saleModule/getSales", { page: page })
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
