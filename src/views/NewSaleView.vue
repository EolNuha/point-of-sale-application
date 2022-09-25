<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center w-1/2 relative">
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
          @keydown="keyEvent"
          @input="
            debounce(() => {
              searchQuery = $event.target.value;
            })
          "
          v-model="searchQuery"
          type="text"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Search"
        />
      </div>
      <div class="search-results" v-if="searchQuery">
        <table
          class="w-full text-sm text-left text-gray-700 dark:text-gray-400 border-solid border-t-0 border-[3px] border-gray-300 dark:border-gray-700 relative"
        >
          <tbody>
            <template v-for="product in searchedProducts" :key="product.id">
              <tr
                class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-700"
                :class="
                  searchedProducts[searchedProductsIndex] === product
                    ? 'bg-blue-100 dark:bg-blue-900'
                    : ''
                "
              >
                <th
                  scope="row"
                  class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  {{ product.id }}
                </th>
                <td class="py-2 px-6">{{ product.barcode }}</td>
                <td class="py-2 px-6">{{ product.name }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
    <div
      class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style mb-[8.5rem]"
    >
      <table
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6"></th>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Product name</th>
            <th scope="col" class="py-3 px-6">Barcode</th>
            <th scope="col" class="py-3 px-6">Quantity</th>
            <th scope="col" class="py-3 px-6">Selling Price</th>
            <th scope="col" class="py-3 px-6"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="product in products" :key="product.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
              :class="
                selectedProduct === product
                  ? 'bg-blue-100 dark:bg-blue-800/25 hover:dark:bg-blue-800/25'
                  : ''
              "
            >
              <td class="py-2 px-6">
                <IconC
                  v-if="selectedProduct === product"
                  iconName="CheckCircleIcon"
                  iconClass="h-6 w-6 fill-blue-500 text-gray-900 dark:text-gray-300 dark:fill-blue-700"
                />
                <IconC
                  v-else
                  iconName="MinusCircleIcon"
                  iconClass="h-6 w-6 text-gray-900 dark:text-gray-300"
                />
              </td>
              <td class="py-2 px-6">
                {{ product.id }}
              </td>
              <td class="py-2 px-6">{{ product.name }}</td>
              <td class="py-2 px-6">{{ product.barcode }}</td>
              <td class="py-2 px-6">
                <input
                  v-model="product.quantity"
                  class="max-w-[100px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block px-2.5 py-1 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @change="() => (total = getProductsTotal())"
                />
              </td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ product.sellingPrice }} €
              </td>
              <td class="py-2 px-6">
                <button
                  class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                  @click="openModal(product)"
                >
                  <IconC
                    iconName="TrashIcon"
                    iconClass="w-5 h-5 text-red-700 cursor-pointer"
                  />
                </button>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div
      class="fixed bottom-0 left-0 flex items-center h-32 bg-gray-100 dark:bg-gray-700 w-full px-3"
    >
      <div
        class="ml-auto flex flex-row items-center text-7xl text-gray-700 dark:text-gray-300"
      >
        Total:
        <div
          class="min-w-64 max-w-md h-28 ml-3 flex items-center justify-center p-2.5 bg-gray-200 dark:bg-gray-800 rounded-lg"
        >
          <span id="total">{{ total }}</span
          >€
        </div>
      </div>
    </div>
    <remove-modal
      :productId="selectedProductToRemove.id"
      title="Product"
      removeRef="remove-modal"
      @remove="removeProduct"
    />
  </div>
</template>

<script>
import RemoveModal from "@/components/modals/RemoveModal.vue";
export default {
  components: {
    RemoveModal,
  },
  name: "NewSaleView",
  data() {
    return {
      isLoading: false,
      selectedProduct: {},
      searchQuery: "",
      searchedProducts: [],
      searchedProductsIndex: 0,
      selectedProductToRemove: {},
      products: [],
      total: "0.00",
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
        if (value === "") this.searchedProductsIndex = 0;
        try {
          await this.$store
            .dispatch("productModule/getProducts", {
              page: 1,
              per_page: 30,
              search: value,
            })
            .then((res) => {
              this.searchedProducts = res.data.data;
            });
        } catch {
          console.log(value);
        }
      },
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
  },
  methods: {
    keyEvent(e) {
      if (
        e.key === "ArrowDown" &&
        this.searchedProductsIndex < this.searchedProducts.length - 1
      ) {
        this.searchedProductsIndex++;
      }
      if (e.key === "ArrowUp" && this.searchedProductsIndex > 0) {
        this.searchedProductsIndex--;
      }
      if (e.key === "Enter" && this.searchQuery) {
        const selectedPr = this.searchedProducts[this.searchedProductsIndex];
        selectedPr.quantity = 1;
        const objectIdx = this.products.findIndex(
          (item) => item.id === selectedPr.id
        );
        if (objectIdx != -1) {
          this.products[objectIdx].quantity++;
        } else {
          this.products.unshift(selectedPr);
        }
        this.total = this.getProductsTotal();
        this.searchQuery = "";
        this.searchedProductsIndex = 0;
      }
    },
    getProductsTotal() {
      const products = this.products;
      const sum = products.reduce((accumulator, object) => {
        return accumulator + object.sellingPrice * object.quantity;
      }, 0);
      return sum.toFixed(2);
    },
    openModal(product) {
      this.selectedProductToRemove = product;
      const el = document.getElementById("remove-modal");
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      mod.show();
    },
    hideModal() {
      const el = document.getElementById("remove-modal");
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      mod.hide();
      document.querySelector("[modal-backdrop]").remove();
    },
    removeProduct(productId) {
      const objectIdx = this.products.findIndex(
        (item) => item.id === productId
      );
      this.products.splice(objectIdx, 1);
      this.total = this.getProductsTotal();
      this.hideModal();
    },
  },
};
</script>

<style lang="scss" scoped>
.search-results {
  position: absolute;
  width: 100%;
  z-index: 1000;
  top: 35px;
}
.min-w-64 {
  min-width: 16rem;
}
#total {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
