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
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search"
          />
        </div>
      </div>
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
          <template v-for="order in orders" :key="order.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <th
                scope="row"
                class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
              >
                {{ order.id }}
              </th>
              <td class="py-2 px-6">{{ order.totalAmount }} €</td>
              <td class="py-2 px-6">{{ order.customerAmount }} €</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ order.changeAmount }} €
              </td>
              <td class="py-2 px-6">
                <button
                  @click="
                    $router.push({
                      name: 'order-view',
                      params: { orderId: order.id },
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
      @pageChange="getOrders($event)"
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
          await this.$store.dispatch("orderModule/getOrders", {
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
    orders() {
      return this.$store.getters["orderModule/getOrdersList"];
    },
    pagination() {
      return this.$store.getters["orderModule/getOrdersPagination"];
    },
  },
  created() {
    window.addEventListener("keydown", (e) => {
      if (e.key == "Delete") {
        const isEmpty = Object.keys(this.selectedProduct).length === 0;
        if (!isEmpty) {
          this.openModal(this.selectedProduct);
        }
      }
    });
    this.reload();
  },
  methods: {
    reload() {
      this.isTableLoading = true;
      this.selectedProduct = {};
      this.$store
        .dispatch("orderModule/getOrders", {
          page: this.currentPage,
        })
        .then(() => {
          this.isTableLoading = false;
        })
        .catch(() => {
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    updateSelectedProduct(product) {
      if (this.selectedProduct.id === product.id) {
        this.selectedProduct = {};
      } else {
        this.selectedProduct = product;
      }
    },
    openModal(product) {
      this.selectedProductToDelete = product;
      const el = document.getElementById("delete-modal");
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      mod.show();
    },
    getOrders(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("orderModule/getOrders", { page: page })
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
