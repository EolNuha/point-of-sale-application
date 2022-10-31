<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center search-input-width">
        <label for="simple-search" class="sr-only">{{ $t("search") }}</label>
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
            class="default-input w-full pl-10"
            :placeholder="$t('search')"
          />
        </div>
      </div>
      <button
        @click="
          $router.push({
            name: 'new-product',
          })
        "
        class="blue-gradient-btn flex items-center text-center"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        {{ $t("createProduct") }}
      </button>
    </div>

    <div class="overflow-hidden rounded-xl my-5 min-h-65 relative">
      <div class="overflow-x-auto overflow-y-hidden scrollbar-style">
        <table
          class="w-full text-sm text-left text-gray-700 dark:text-gray-400"
        >
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="products.length === 0 && !isTableLoading"
            pluralText="Products"
            singularText="Product"
            :search="searchQuery"
            routeName="new-product"
          />
          <thead
            class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400 cursor-default"
          >
            <tr>
              <th scope="col" class="py-3 px-6"></th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('id')"
              >
                <div class="flex justify-between items-center">
                  ID
                  <template v-if="sortColumn === 'id'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('name')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("productName") }}
                  <template v-if="sortColumn === 'name'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('barcode')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("barcode") }}
                  <template v-if="sortColumn === 'barcode'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('purchased_price')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("purchasedPrice") }}
                  <template v-if="sortColumn === 'purchased_price'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('selling_price')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("sellingPrice") }}
                  <template v-if="sortColumn === 'selling_price'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('stock')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("stock") }}
                  <template v-if="sortColumn === 'stock'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('tax')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("tax") }}
                  <template v-if="sortColumn === 'tax'">
                    <IconC
                      iconName="ArrowLongDownIcon"
                      iconClass="w-4 h-4"
                      v-if="sortDir === 'desc'"
                    />
                    <IconC
                      iconName="ArrowLongUpIcon"
                      iconClass="w-4 h-4"
                      v-else
                    />
                  </template>
                </div>
              </th>
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
                    iconClass="h-5 w-5 fill-blue-500 text-gray-900 dark:text-gray-300 dark:fill-blue-700"
                  />
                  <IconC
                    v-else
                    iconName="MinusCircleIcon"
                    iconClass="h-5 w-5 text-gray-900 dark:text-gray-300"
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
                <td class="py-2 px-6 max-w-xs">
                  {{ product.purchasedPrice }} €
                </td>
                <td class="py-2 px-6 max-w-xs">{{ product.sellingPrice }} €</td>
                <td class="py-2 px-6">
                  <div
                    class="flex items-center"
                    :id="`product-${product.id}-tooltip-btn`"
                    @mouseover="
                      $showTooltip({
                        targetEl: `product-${product.id}-tooltip`,
                        triggerEl: `product-${product.id}-tooltip-btn`,
                      })
                    "
                    :class="stockStatus(product.stock).color"
                  >
                    &#9679; {{ stockStatus(product.stock).text }}
                  </div>
                  <div
                    :id="`product-${product.id}-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
                  >
                    {{ product.stock }}
                    <div class="tooltip-arrow" data-popper-arrow></div>
                  </div>
                </td>
                <td class="py-2 px-6 max-w-xs">{{ product.tax }}%</td>
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
                    @click="deleteProduct(product)"
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
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getProducts($event)"
    />
    <delete-modal
      :productId="selectedProductToDelete.id"
      deleteAction="productModule/deleteProduct"
      getAction="productModule/getProducts"
      :title="$t('product')"
      deleteRef="delete-modal"
      @reload="getProducts(currentPage)"
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
      sortColumn: null,
      sortDir: "desc",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        this.currentPage = 1;
        try {
          await this.$store.dispatch("productModule/getProducts", {
            page: this.currentPage,
            search: value,
            sort_column: this.sortColumn,
            sort_dir: this.sortDir,
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
          this.deleteProduct(this.selectedProduct);
        }
      }
    });
    this.getProducts(this.currentPage);
  },
  methods: {
    updateSelectedProduct(product) {
      if (this.selectedProduct.id === product.id) {
        this.selectedProduct = {};
      } else {
        this.selectedProduct = product;
      }
    },
    deleteProduct(product) {
      this.selectedProductToDelete = product;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-product-modal-btn");
    },
    getProducts(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("productModule/getProducts", {
          page: page,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    stockStatus(v) {
      let color;
      let text;
      if (v >= 50) {
        color = "text-green-500";
        text = this.$t("inStock");
      } else if (v < 50 && v > 0) {
        color = "text-yellow-400";
        text = this.$t("lowStock");
      } else if (v <= 0) {
        color = "text-red-700";
        text = this.$t("outStock");
      }
      return { color, text };
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getProducts(this.currentPage);
    },
  },
};
</script>
