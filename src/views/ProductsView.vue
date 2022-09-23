<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between">
      <button
        @click="
          $router.push({
            name: 'products-create',
          })
        "
        class="flex items-center text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-auto px-5 py-1.5 flex justify-center items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        Create Product
      </button>
      <div class="flex items-center w-64">
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
            <th scope="col" class="py-3 px-6"></th>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Product name</th>
            <th scope="col" class="py-3 px-6">Barcode</th>
            <th scope="col" class="py-3 px-6">Purchased Price</th>
            <th scope="col" class="py-3 px-6">Selling Price</th>
            <th scope="col" class="py-3 px-6">Stock</th>
            <th scope="col" class="py-3 px-6"></th>
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
              <td class="py-2 px-6" @click="updateSelectedProduct(product)">
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
              <th
                scope="row"
                class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
              >
                {{ product.id }}
              </th>
              <td class="py-2 px-6">{{ product.name }}</td>
              <td class="py-2 px-6">{{ product.barcode }}</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ product.purchasedPrice }} €
              </td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ product.sellingPrice }} €
              </td>
              <td class="py-2 px-6">
                <div
                  class="flex items-center"
                  :class="stockStatus(product.stock).color"
                >
                  &#9679; {{ stockStatus(product.stock).text }}
                </div>
              </td>
              <td
                class="py-2 px-6"
                @click="
                  $router.push({
                    name: 'product-view',
                    params: { productId: product.id },
                  })
                "
              >
                <button
                  class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                >
                  <IconC
                    iconType="solid"
                    iconName="PencilIcon"
                    iconClass="w-5 h-5 text-blue-700 cursor-pointer"
                  />
                </button>
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
    <div class="flex justify-between items-center">
      <div class="text-gray-700 dark:text-gray-400">
        Viewing page
        <span
          class="bg-white dark:bg-gray-700 rounded-lg font-semibold text-gray-900 dark:text-white p-2.5"
          >{{ currentPage }}</span
        >
        with {{ pagination.items }} items of total {{ pagination.total }}
      </div>
      <div aria-label="Page navigation" v-if="!(pagination.pages === 1)">
        <ul class="inline-flex items-center -space-x-px">
          <li
            @click="getProducts(pagination.prev_num)"
            v-if="pagination.has_prev"
          >
            <a
              href="#"
              onclick="return false;"
              disabled
              class="block py-2 px-3 ml-0 leading-tight text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
            >
              <span class="sr-only">Previous</span>
              <IconC
                iconType="solid"
                icontType="20"
                iconName="ChevronLeftIcon"
                iconClass="w-5 h-5"
              />
            </a>
          </li>
          <li
            v-for="page in pagination.page_range"
            :key="page"
            @click="getProducts(page)"
          >
            <a
              href="#"
              onclick="return false;"
              aria-current="page"
              :class="
                page === currentPage
                  ? 'py-2 px-3 leading-tight text-blue-600 bg-blue-50 border border-blue-300 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white'
                  : 'py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white'
              "
              >{{ page }}</a
            >
          </li>
          <li
            @click="getProducts(pagination.next_num)"
            v-if="pagination.has_next"
          >
            <a
              href="#"
              onclick="return false;"
              class="block py-2 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
            >
              <span class="sr-only">Next</span>
              <IconC
                iconType="solid"
                icontType="20"
                iconName="ChevronRightIcon"
                iconClass="w-5 h-5"
              />
            </a>
          </li>
        </ul>
      </div>
    </div>
    <delete-modal
      :productId="selectedProductToDelete.id"
      deleteAction="productModule/deleteProduct"
      getAction="productModule/getProducts"
      title="Product"
      deleteRef="delete-modal"
      @reload="reload"
    >
    </delete-modal>
  </div>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
export default {
  components: {
    DeleteModal,
  },
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
          await this.$store.dispatch("productModule/getProducts", {
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
    products() {
      return this.$store.getters["productModule/getProductsList"];
    },
    pagination() {
      return this.$store.getters["productModule/getProductsPagination"];
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
      this.$store
        .dispatch("productModule/getProducts", {
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
    getProducts(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("productModule/getProducts", { page: page })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    stockStatus(v) {
      console.log(v);
      let color;
      let text;
      if (v >= 50) {
        color = "text-green-500";
        text = "In stock";
      } else if (v < 50 && v > 0) {
        color = "text-yellow-400";
        text = "Low stock";
      } else if (v <= 0) {
        color = "text-red-700";
        text = "Out of stock";
      }
      return { color, text };
    },
  },
};
</script>
