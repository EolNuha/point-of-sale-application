<!-- eslint-disable no-undef -->
<template>
  <div class="main-div">
    <div class="full-layout flex flex-col">
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
              @input="searchQuery = $event.target.value"
              type="text"
              class="default-input w-full pl-10"
              :placeholder="$t('search')"
            />
          </div>
        </div>
        <div class="flex flex-row items-center gap-2">
          <button
            @click="deleteProducts"
            v-if="$can('execute', 'products') && selectedProducts?.length > 0"
            class="red-gradient-btn flex items-center text-center"
          >
            <IconC iconName="TrashIcon" iconClass="w-5 h-5 mr-2" />
            {{ $t("delete") }} ({{ selectedProducts?.length }})
          </button>
          <button
            @click="
              $router.push({
                name: 'new-product',
              })
            "
            v-if="$can('write', 'products')"
            class="theme-gradient-btn flex items-center text-center"
          >
            <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
            {{ $t("createProduct") }}
          </button>
          <button
            id="dropdownProductsExcelMenuBtn"
            @click="
              $toggleDropdown({
                targetEl: `dropdownProductsExcelMenu`,
                triggerEl: `dropdownProductsExcelMenuBtn`,
                placement: `top`,
              })
            "
            class="green-gradient-btn inline-flex items-center text-center"
          >
            <div class="inline-flex flex-row">
              <IconC
                iconType="custom"
                iconName="ExcelFileIcon"
                iconClass="w-5 h-5 fill-white mr-2"
              />
              Excel
            </div>
          </button>
          <div
            id="dropdownProductsExcelMenu"
            class="hidden z-10 flex flex-col gap-[2px] w-44 bg-white rounded shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800 dark:divide-gray-600"
            style="inset: 0px auto auto -10px !important"
          >
            <button
              @click="downloadExcel()"
              class="gray-outline-btn inline-flex items-center text-center w-full text-green-500"
              :disabled="!(products?.length > 0)"
            >
              <div
                class="inline-flex flex-row"
                role="status"
                v-if="isExcelLoading"
              >
                <IconC
                  iconType="custom"
                  iconName="SpinnerIcon"
                  iconClass="mr-2 w-5 h-5 text-gray-200 animate-spin fill-green-500"
                />
                {{ $t("downloading") }}...
                <span class="sr-only">Loading...</span>
              </div>
              <div class="inline-flex flex-row" v-else>
                <IconC
                  iconType="custom"
                  iconName="ExcelFileIcon"
                  iconClass="w-5 h-5 fill-green-500 mr-2"
                />
                {{ $t("download") }} Excel
              </div>
            </button>
            <button
              @click="$openModal(uploadExcelRef)"
              class="gray-outline-btn inline-flex items-center text-center w-full text-green-500"
            >
              <div class="inline-flex flex-row">
                <IconC
                  iconType="custom"
                  iconName="ExcelFileIcon"
                  iconClass="w-5 h-5 fill-green-500 mr-2"
                />
                {{ $t("upload") }} Excel
              </div>
            </button>
          </div>
        </div>
      </div>

      <div class="overflow-hidden rounded my-5 flex grow relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style grow">
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="products?.length === 0 && !isTableLoading"
            pluralText="Products"
            singularText="Product"
            :search="searchQuery"
            routeName="new-product"
          />
          <table
            class="bg-white dark:bg-neutral-800 w-full text-sm text-left text-gray-700 dark:text-gray-400 overflow-hidden rounded"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
            >
              <tr>
                <th
                  scope="col"
                  class="py-0 px-6"
                  v-if="$can('execute', 'products')"
                >
                  <button
                    @click="
                      () =>
                        areAllSelected
                          ? (selectedProducts = [])
                          : (selectedProducts = JSON.parse(
                              JSON.stringify(products.map((obj) => obj.id))
                            ))
                    "
                    class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                  >
                    <input
                      type="checkbox"
                      class="rounded cursor-pointer text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
                      :checked="areAllSelected"
                      :indeterminate="
                        selectedProducts.length > 0 && !areAllSelected
                      "
                    />
                  </button>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('name')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("product_name") }}
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('purchased_price')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("purchased_price") }}
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('selling_price')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("selling_price") }}
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                <th
                  scope="col"
                  class="py-3 px-6"
                  v-if="$can('execute', 'products')"
                ></th>
              </tr>
            </thead>
            <tbody>
              <template v-for="product in products" :key="product.id">
                <tr
                  class="border-b dark:border-gray-700"
                  :class="
                    selectedProducts.some((obj) => obj === product.id)
                      ? 'bg-theme-100 dark:bg-theme-400 dark:text-black font-bold'
                      : 'bg-white dark:bg-neutral-900 hover:bg-neutral-100/75 dark:hover:bg-neutral-900/[.5]'
                  "
                >
                  <td class="py-2 px-6" v-if="$can('execute', 'products')">
                    <button
                      @click="toggleSelectProduct(product.id)"
                      class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                    >
                      <input
                        type="checkbox"
                        class="rounded cursor-pointer text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
                        :checked="
                          selectedProducts.some((obj) => obj === product.id)
                        "
                      />
                    </button>
                  </td>
                  <td scope="row" class="py-2 px-6">
                    {{ product.id }}
                  </td>
                  <td class="py-2 px-6">{{ product.name }}</td>
                  <td class="py-2 px-6">{{ product.barcode }}</td>
                  <td class="py-2 px-6 max-w-xs">
                    {{ product.purchased_price }} €
                  </td>
                  <td class="py-2 px-6 max-w-xs">
                    {{ product.selling_price }} €
                  </td>
                  <td class="py-2 px-6">
                    <div
                      class="flex items-center bg-white dark:bg-neutral-900 p-1.5 rounded"
                      :id="`product-${product.id}-tooltip-btn`"
                      @mouseover="
                        $showTooltip({
                          targetEl: `product-${product.id}-tooltip`,
                          triggerEl: `product-${product.id}-tooltip-btn`,
                        })
                      "
                      :class="stockStatus(product.stock).color"
                    >
                      &#9679; {{ product.stock }}
                    </div>
                    <div
                      :id="`product-${product.id}-tooltip`"
                      role="tooltip"
                      class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 rounded shadow-sm opacity-0 tooltip"
                    >
                      {{ stockStatus(product.stock).text }}
                    </div>
                  </td>
                  <td class="py-2 px-6 max-w-xs">
                    <div class="py-2.5">{{ product.tax }}%</div>
                  </td>
                  <td
                    class="py-2 px-6 w-1.5"
                    v-if="$can('execute', 'products')"
                  >
                    <button
                      class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                      :id="`product-${product.id}-btn`"
                      @click="
                        $toggleDropdown({
                          targetEl: `product-${product.id}-menu`,
                          triggerEl: `product-${product.id}-btn`,
                          placementEl: 'left',
                        })
                      "
                    >
                      <IconC
                        iconName="EllipsisVerticalIcon"
                        iconClass="w-5 h-5 cursor-pointer"
                      />
                    </button>
                    <div
                      :id="`product-${product.id}-menu`"
                      class="hidden z-10 w-32 bg-white rounded shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800"
                      style="inset: 0px auto auto -300px !important"
                    >
                      <ul
                        class="py-1 text-sm font-normal text-gray-700 cursor-pointer divide-y divide-gray-300 dark:divide-gray-700"
                        aria-labelledby="dropdownDefault"
                      >
                        <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'product-view',
                              params: { productId: product.id },
                            })
                          "
                        >
                          <IconC
                            iconType="solid"
                            iconName="PencilIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("edit") }}
                        </li>
                        <li
                          class="inline-flex text-red-700 dark:text-red-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="deleteProduct(product)"
                        >
                          <IconC
                            iconName="TrashIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("delete") }}
                        </li>
                      </ul>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
      <delete-modal
        :itemId="{ products: selectedProducts }"
        deleteAction="productModule/deleteProducts"
        :title="$t('products')"
        deleteRef="delete-multiple-modal"
        @reload="
          getProducts(currentPage);
          selectedProducts = [];
        "
      >
      </delete-modal>
      <delete-modal
        :itemId="selectedProductToDelete.id"
        deleteAction="productModule/deleteProduct"
        :title="$t('product')"
        deleteRef="delete-modal"
        @reload="getProducts(currentPage)"
      >
      </delete-modal>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="
        getProducts($event);
        selectedProducts = [];
      "
    />
    <upload-excel-modal
      :key="uploadExcelRef"
      :modalRef="uploadExcelRef"
      @reload="getProducts(currentPage)"
    />
  </div>
</template>

<script>
import debounce from "lodash/debounce";
import DeleteModal from "@/components/modals/DeleteModal.vue";
import JsonToExcel from "@/services/mixins/JsonToExcel";
import UploadExcelModal from "@/components/modals/UploadExcelModal.vue";
export default {
  components: {
    DeleteModal,
    UploadExcelModal,
  },
  data() {
    return {
      uploadExcelRef: "upload-excel-ref",
      isTableLoading: true,
      isExcelLoading: false,
      selectedProducts: [],
      selectedProductToDelete: {},
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      allProducts: [],
      debouncedGetProducts: null,
    };
  },
  mixins: [JsonToExcel],
  watch: {
    searchQuery: {
      async handler() {
        this.currentPage = 1;
        this.debouncedGetProducts(1);
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
    areAllSelected() {
      const productsCopy = JSON.parse(
        JSON.stringify(this.products.map((obj) => obj.id))
      );
      const selectedItemsCopy = JSON.parse(
        JSON.stringify(this.selectedProducts)
      );
      return (
        JSON.stringify(productsCopy.sort((a, b) => (a > b ? 1 : -1))) ===
          JSON.stringify(selectedItemsCopy.sort((a, b) => (a > b ? 1 : -1))) &&
        this.products?.length !== 0
      );
    },
  },
  async created() {
    this.debouncedGetProducts = debounce(this.getProducts, 500);
    window.addEventListener("keydown", (e) => {
      if (e.key == "Delete") {
        const isEmpty = this.selectedProducts?.length === 0;
        if (!isEmpty) {
          this.deleteProducts();
        }
      }
    });
    await this.getProducts(this.currentPage);
  },
  methods: {
    toggleSelectProduct(product) {
      const idx = this.selectedProducts.findIndex((x) => x === product);
      if (idx !== -1) this.selectedProducts.splice(idx, 1);
      if (idx === -1) this.selectedProducts.push(product);
    },
    deleteProduct(product) {
      this.selectedProductToDelete = product;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
    deleteProducts() {
      this.$openModal("delete-multiple-modal");
      this.$putOnFocus("delete-multiple-modal-btn");
    },
    async getProducts(page) {
      this.isTableLoading = true;
      await this.$store
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
    async getAllProducts() {
      await this.$store
        .dispatch("productModule/getAllProducts", {
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then((res) => {
          this.allProducts = res.data;
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
    async downloadExcel() {
      this.isExcelLoading = true;
      await this.getAllProducts();

      await this.jsonToExcel(this.allProducts, this.$t("products"));
      this.isExcelLoading = false;
    },
  },
};
</script>

<style lang="scss" scoped>
#dropdownProductsExcelMenu {
  inset: 0px auto auto -20px !important;
}
</style>
