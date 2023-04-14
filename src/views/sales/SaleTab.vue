<template>
  <div class="p-4" :id="id">
    <div class="flex justify-between gap-2">
      <div class="flex items-center search-input-width relative">
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
            @keydown="keyEvent"
            v-model="searchQuery"
            type="text"
            class="default-input w-full pl-10"
            :placeholder="$t('search')"
          />
        </div>
        <div class="search-results" v-if="searchQuery">
          <table
            class="w-full bg-white dark:bg-neutral-700 text-sm text-left text-gray-700 dark:text-gray-400 border-solid border-t-0 border-[3px] border-gray-300 dark:border-neutral-700 relative"
          >
            <tbody>
              <template v-for="product in searchedProducts" :key="product.id">
                <tr
                  @click="onSearchedProductClick(product)"
                  class="border-b dark:border-neutral-700 cursor-default"
                  :class="
                    searchedProducts[searchedProductsIndex] === product
                      ? 'bg-theme-100 dark:bg-theme-400 dark:text-black bg-opacity-25 font-bold'
                      : 'bg-white dark:bg-neutral-900 hover:bg-neutral-100/75 hover:dark:bg-neutral-900/[.5]'
                  "
                >
                  <th
                    scope="row"
                    class="py-2 px-6 font-medium whitespace-nowrap"
                  >
                    {{ product.id }}
                  </th>
                  <td class="py-2 px-6">{{ product.name }}</td>
                  <td class="py-2 px-6">{{ product.barcode }}</td>
                  <td class="py-2 px-6">{{ product.sellingPrice }} €</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
      <div class="flex items-center gap-2 text-gray-700 dark:text-gray-300">
        <input
          id="regular-sale"
          type="checkbox"
          class="rounded text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
          v-model="isRegular"
        />
        <label for="regular-sale" class="flex items-center gap-2">
          {{ $t("regular") }}
          <IconC iconType="solid" iconName="PrinterIcon" iconClass="w-5 h-5" />
        </label>
      </div>
    </div>
    <div
      class="overflow-x-auto relative rounded my-5 scrollbar-style mb-[8.5rem]"
    >
      <table
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <thead
          class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6"></th>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">{{ $t("productName") }}</th>
            <th scope="col" class="py-3 px-6">{{ $t("barcode") }}</th>
            <th scope="col" class="py-3 px-6">{{ $t("quantity") }}</th>
            <th scope="col" class="py-3 px-6">{{ $t("sellingPrice") }}</th>
            <!-- <th scope="col" class="py-3 px-6"></th> -->
          </tr>
        </thead>
        <tbody>
          <template v-for="product in products" :key="product.id">
            <tr
              class="border-b dark:border-neutral-700 cursor-default"
              :class="
                isSelected(product.id)
                  ? 'bg-theme-100 dark:bg-theme-400 dark:text-black bg-opacity-25 font-bold'
                  : 'bg-white dark:bg-neutral-900 hover:bg-neutral-100/75 dark:hover:bg-neutral-900/[.5]'
              "
            >
              <td class="py-2 px-6">
                <button
                  @click.stop
                  @click="toggleSelectProduct(product)"
                  class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                >
                  <input
                    type="checkbox"
                    class="rounded cursor-pointer text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
                    :checked="isSelected(product.id)"
                  />
                </button>
              </td>
              <td class="py-2 px-6">
                {{ product.id }}
              </td>
              <td class="py-2 px-6">{{ product.name }}</td>
              <td class="py-2 px-6">{{ product.barcode }}</td>
              <td class="py-2 px-6">
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  :id="`product-${product.id}-quantity`"
                  v-model="product.quantity"
                  class="max-w-[100px] bg-neutral-50 border border-gray-300 text-gray-900 text-sm rounded focus:ring-theme-500 focus:border-theme-500 block w-full px-2 py-1 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
                  @change="
                    () =>
                      product.quantity
                        ? (product.quantity = product.quantity)
                        : (product.quantity = 1)
                  "
                  @focus="$event.target.select()"
                />
              </td>
              <td class="py-2 px-6 max-w-xs">{{ product.sellingPrice }} €</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div
      class="absolute bottom-0 left-0 right-0 flex items-center justify-between h-28 bg-neutral-100 dark:bg-neutral-700 px-2 overflow-x-auto overflow-y-hidden scrollbar-style"
    >
      <div class="flex flex-row items-center">
        <button
          :disabled="products?.length === 0"
          @click="finishSaleModal()"
          type="button"
          id="finishSale"
          class="flex justify-center items-center flex-col gap-2 text-center text-gray-900 bg-neutral-200 border border-gray-300 focus:outline-none hover:bg-neutral-100 focus:ring-4 focus:ring-gray-200 font-medium rounded text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-neutral-800 dark:text-white dark:border-gray-600 dark:hover:bg-neutral-800/75 dark:hover:border-gray-600 dark:focus:ring-gray-700"
        >
          <IconC iconType="solid" iconName="CheckIcon" iconClass="w-5 h-5" />
          {{ $t("finish") }} (F8)
        </button>
        <button
          :disabled="products?.length === 0"
          @click="openRemoveModal(JSON.parse(JSON.stringify(products)))"
          type="button"
          id="clearAll"
          class="flex justify-center items-center flex-col gap-2 text-center text-gray-900 bg-neutral-200 border border-gray-300 focus:outline-none hover:bg-neutral-100 focus:ring-4 focus:ring-gray-200 font-medium rounded text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-neutral-800 dark:text-white dark:border-gray-600 dark:hover:bg-neutral-800/75 dark:hover:border-gray-600 dark:focus:ring-gray-700"
        >
          <IconC iconName="TrashIcon" iconClass="w-5 h-5" />
          {{ $t("clearAll") }} (F10)
        </button>
      </div>
      <div
        class="flex flex-row items-center text-3xl md:text-7xl text-gray-700 dark:text-gray-300"
      >
        {{ $t("total") }}:
        <div
          class="min-w-[8rem] md:min-w-64 max-w-[12rem] md:max-w-md h-24 ml-3 flex items-center justify-center p-2.5 bg-neutral-200 dark:bg-neutral-800 rounded"
        >
          <span>{{ total }}</span
          >€
        </div>
      </div>
    </div>
    <remove-modal
      :key="removeModalRef"
      :value="selectedProductsToRemove"
      title="Product"
      :removeRef="removeModalRef"
      @remove="removeProducts($event)"
    />
    <finish-sale-modal
      :key="finishSaleModalRef"
      :isLoading="isFinishSaleLoading"
      :modalRef="finishSaleModalRef"
      :total="total"
      @submit="finishSale"
    />
  </div>
</template>

<script>
import RemoveModal from "@/components/modals/RemoveModal.vue";
import FinishSaleModal from "@/components/modals/FinishSaleModal.vue";
export default {
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  components: {
    RemoveModal,
    FinishSaleModal,
  },
  data() {
    return {
      isFinishSaleLoading: false,
      removeModalRef: `${this.id}-remove-modal`,
      finishSaleModalRef: `${this.id}-finish-sale-modal`,
      selectedProducts: [],
      selectedProductsToRemove: [],
      searchQuery: "",
      searchedProducts: [],
      searchedProductsIndex: 0,
      lastSearchedProduct: {},
      isRegular: false,
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        if (value === "") {
          this.searchedProductsIndex = 0;
          this.searchedProducts = [];
          return;
        }
        try {
          await this.$store
            .dispatch("productModule/getProducts", {
              page: 1,
              per_page: 10,
              search: value,
              sort_column: "name",
              sort_dir: "asc",
            })
            .then((res) => {
              this.searchedProducts = res.data.data;
            });
        } catch {
          console.log();
        }
      },
    },
  },
  computed: {
    isSelected() {
      return (id) => this.selectedProducts?.some((obj) => obj?.id === id);
    },
    products: {
      get() {
        return this.$store.getters["saleModule/getCurrentSaleProducts"](
          this.id
        );
      },
      set(v) {
        this.$store.commit("saleModule/SET_CURRENT_SALES", {
          tab: this.id,
          products: v,
        });
      },
    },
    total() {
      const products = this.products;
      const sum = products?.reduce((accumulator, object) => {
        return accumulator + object.sellingPrice * object.quantity;
      }, 0);
      return sum?.toFixed(2);
    },
  },
  created() {
    window.addEventListener("keydown", (e) => {
      if (e.key == "Delete" && this.id === this.$parent.activeTab) {
        const isEmpty = this.selectedProducts?.length === 0;
        if (!isEmpty) {
          this.openRemoveModal(this.selectedProducts);
        }
      }
      if (e.key == "F8" && this.id === this.$parent.activeTab) {
        const isProductsEmpty = this.products?.length === 0;
        if (!isProductsEmpty) {
          this.finishSaleModal();
        }
      }
      if (e.key == "F10" && this.id === this.$parent.activeTab) {
        const isProductsEmpty = this.products?.length === 0;
        if (!isProductsEmpty) {
          this.openRemoveModal(JSON.parse(JSON.stringify(this.products)));
        }
      }
    });
  },
  methods: {
    keyEvent(e) {
      if (
        e.key === "ArrowDown" &&
        this.searchedProductsIndex < this.searchedProducts?.length - 1
      ) {
        this.searchedProductsIndex++;
      }
      if (e.key === "ArrowUp" && this.searchedProductsIndex > 0) {
        e.preventDefault();
        this.searchedProductsIndex--;
      }
      if (e.key === "Enter" && !this.searchQuery) {
        const productId = this.lastSearchedProduct.id;
        this.$putOnFocus(`product-${productId}-quantity`);
      }
      if (e.key === "Enter" && this.searchQuery) {
        const selectedPr = this.searchedProducts[this.searchedProductsIndex];
        if (!selectedPr) e.target.select();
        else this.onSearchedProductClick(selectedPr);
      }
    },
    onSearchedProductClick(product) {
      this.lastSearchedProduct = product;
      product.quantity = 1;
      const objectIdx = this.products?.findIndex(
        (item) => item.id === product.id
      );
      if (objectIdx != -1) {
        this.products[objectIdx].quantity++;
      } else {
        this.products.unshift(product);
      }
      this.searchQuery = "";
      this.searchedProductsIndex = 0;
      this.searchedProducts = [];
    },
    openRemoveModal(products) {
      this.selectedProductsToRemove = products;
      this.$openModal(this.removeModalRef);
      this.$putOnFocus(this.removeModalRef + "_remove_btn");
    },
    removeProducts(products) {
      products.forEach((item) => {
        this.products.splice(
          this.products?.findIndex((x) => x.id === item.id),
          1
        );
      });
      this.selectedProducts = [];
      this.$hideModal(this.removeModalRef);
    },
    finishSaleModal() {
      this.$openModal(this.finishSaleModalRef);
      this.$putOnFocus(this.finishSaleModalRef + "_customer_amount");
    },
    finishSale(e) {
      this.isFinishSaleLoading = true;
      const data = {
        products: this.products,
        customerAmount: parseFloat(e).toFixed(2),
        changeAmount: (parseFloat(e) - this.total).toFixed(2),
        isRegular: this.isRegular,
      };
      this.$store
        .dispatch("saleModule/createSale", data)
        .then(() => {
          this.isFinishSaleLoading = false;
          this.products = [];
          this.selectedProducts = [];
          this.$hideModal(this.finishSaleModalRef);
          this.$toast.success(this.$t("saleSuccess"));
        })
        .catch(() => {
          this.isFinishSaleLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    toggleSelectProduct(notification) {
      const idx = this.selectedProducts?.findIndex(
        (x) => x?.id === notification.id
      );
      if (idx !== -1) this.selectedProducts.splice(idx, 1);
      if (idx === -1) this.selectedProducts.push(notification);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "/src/styles/views/_newsale.scss";
</style>
