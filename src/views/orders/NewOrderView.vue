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
          v-model="searchQuery"
          type="text"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Search"
        />
      </div>
      <div class="search-results" v-if="searchQuery">
        <table
          class="w-full bg-white dark:bg-gray-900 text-sm text-left text-gray-700 dark:text-gray-400 border-solid border-t-0 border-[3px] border-gray-300 dark:border-gray-700 relative"
        >
          <tbody>
            <template v-for="product in searchedProducts" :key="product.id">
              <tr
                @click="onSearchedProductClick(product)"
                class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:bg-gray-100/75 hover:dark:bg-gray-800/50"
                :class="
                  searchedProducts[searchedProductsIndex] === product
                    ? 'bg-blue-100 dark:bg-blue-900 hover:bg-blue-200/75 hover:dark:bg-blue-800/50'
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
              <td class="py-2 px-6">
                {{ product.id }}
              </td>
              <td class="py-2 px-6">{{ product.name }}</td>
              <td class="py-2 px-6">{{ product.barcode }}</td>
              <td class="py-2 px-6">
                <input
                  :id="`product-${product.id}-quantity`"
                  v-model="product.quantity"
                  class="max-w-[100px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block px-2.5 py-1 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  @change="() => (total = getProductsTotal())"
                  @focus="$event.target.select()"
                />
              </td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ product.sellingPrice }} €
              </td>
              <td class="py-2 px-6">
                <button
                  class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                  @click="openRemoveModal(product)"
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
      class="fixed bottom-0 left-[16rem] right-0 flex items-center justify-between h-28 bg-gray-100 dark:bg-gray-700 px-2"
    >
      <button
        :disabled="products.length === 0"
        @click="finishOrderModal()"
        type="button"
        id="finishOrder"
        class="flex justify-center items-center flex-col text-center text-gray-900 bg-gray-200 border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-800/75 dark:hover:border-gray-600 dark:focus:ring-gray-700"
      >
        <IconC
          iconType="solid"
          iconSize="20"
          iconName="CheckIcon"
          iconClass="w-6 h-6"
        />
        Finish (F8)
      </button>
      <div
        class="flex flex-row items-center text-7xl text-gray-700 dark:text-gray-300"
      >
        Total:
        <div
          class="min-w-64 max-w-md h-24 ml-3 flex items-center justify-center p-2.5 bg-gray-200 dark:bg-gray-800 rounded-lg"
        >
          <span id="total">{{ total }}</span
          >€
        </div>
      </div>
    </div>
    <remove-modal
      :productId="selectedProductToRemove.id"
      title="Product"
      :removeRef="removeModalRef"
      @remove="removeProduct"
    />
    <finish-order-modal
      :isLoading="isFinishOrderLoading"
      :modalRef="finishOrderModalRef"
      :total="total"
      @submit="finishOrder"
    />
  </div>
</template>

<script>
import RemoveModal from "@/components/modals/RemoveModal.vue";
import FinishOrderModal from "@/components/modals/FinishOrderModal.vue";
export default {
  components: {
    RemoveModal,
    FinishOrderModal,
  },
  name: "NewOrderView",
  data() {
    return {
      isFinishOrderLoading: false,
      removeModalRef: "remove-modal",
      finishOrderModalRef: "finish-order-modal",
      selectedProduct: {},
      searchQuery: "",
      searchedProducts: [],
      searchedProductsIndex: 0,
      selectedProductToRemove: {},
      lastSearchedProduct: {},
      products: [],
      total: "0.00",
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
          console.log();
        }
      },
    },
  },
  created() {
    window.addEventListener("keydown", (e) => {
      if (e.key == "Delete") {
        const isEmpty = Object.keys(this.selectedProduct).length === 0;
        if (!isEmpty) {
          this.openRemoveModal(this.selectedProduct);
        }
      }
      if (e.key == "F8") {
        const isProductsEmpty = this.products.length === 0;
        if (!isProductsEmpty) {
          this.finishOrderModal();
        }
      }
    });
  },
  async beforeRouteLeave(to, from, next) {
    if (!(this.products.length === 0)) {
      await this.$swal({
        html: "<p class='text-gray-500 dark:text-gray-300'>The order is not finished, are you sure you want to continue?</p>",
        icon: "info",
        confirmButtonText: "Confirm",
        showCancelButton: true,
        showCloseButton: true,
        focusConfirm: true,
        customClass: {
          popup: "bg-gray-300 dark:bg-gray-800",
          header: "bg-gray-300 dark:bg-gray-800",
          confirmButton:
            "text-white !bg-blue-600 h-10 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 text-sm font-medium rounded-lg inline-flex items-center justify-center px-5 py-2.5",
          cancelButton:
            "text-gray-500 bg-white h-10 hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border !border-gray-200 text-sm font-medium px-5 py-2.5 !hover:text-gray-900 inline-flex items-center justify-center !dark:bg-gray-700 !dark:text-gray-300 !dark:border-gray-500 !dark:hover:text-white !dark:hover:bg-gray-600 !dark:focus:ring-gray-600 mr-2",
        },
      }).then((result) => {
        if (result.isDenied || result.isDismissed) {
          return;
        } else {
          next();
        }
      });
    } else {
      next();
    }
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
      if (e.key === "Enter" && !this.searchQuery) {
        const productId = this.lastSearchedProduct.id;
        this.$putOnFocus(`product-${productId}-quantity`);
      }
      if (e.key === "Enter" && this.searchQuery) {
        const selectedPr = this.searchedProducts[this.searchedProductsIndex];
        this.onSearchedProductClick(selectedPr);
      }
    },
    onSearchedProductClick(product) {
      this.lastSearchedProduct = product;
      product.quantity = 1;
      const objectIdx = this.products.findIndex(
        (item) => item.id === product.id
      );
      if (objectIdx != -1) {
        this.products[objectIdx].quantity++;
      } else {
        this.products.unshift(product);
      }
      this.total = this.getProductsTotal();
      this.searchQuery = "";
      this.searchedProductsIndex = 0;
    },
    getProductsTotal() {
      const products = this.products;
      const sum = products.reduce((accumulator, object) => {
        return accumulator + object.sellingPrice * object.quantity;
      }, 0);
      return sum.toFixed(2);
    },
    updateSelectedProduct(product) {
      if (this.selectedProduct.id === product.id) {
        this.selectedProduct = {};
      } else {
        this.selectedProduct = product;
      }
    },
    openRemoveModal(product) {
      this.selectedProductToRemove = product;
      this.$openModal(this.removeModalRef);
      this.$putOnFocus("remove-modal-btn");
    },
    removeProduct(productId) {
      const objectIdx = this.products.findIndex(
        (item) => item.id === productId
      );
      this.products.splice(objectIdx, 1);
      this.total = this.getProductsTotal();
      this.selectedProduct = {};
      this.$hideModal(this.removeModalRef);
    },
    finishOrderModal() {
      this.$openModal(this.finishOrderModalRef);
      this.$putOnFocus("customer_amount");
    },
    finishOrder(e) {
      this.isFinishOrderLoading = true;
      document.getElementById("finishOrder").blur();
      const data = {
        products: this.products,
        totalAmount: this.total,
        customerAmount: parseFloat(e).toFixed(2),
        changeAmount: (parseFloat(e) - this.total).toFixed(2),
      };
      this.$store
        .dispatch("orderModule/createOrder", data)
        .then(() => {
          this.isFinishOrderLoading = false;
          this.products = [];
          this.selectedProduct = {};
          this.total = (0).toFixed(2);
          this.$hideModal(this.finishOrderModalRef);
          this.$toast.success("Order was successful!");
        })
        .catch(() => {
          this.isFinishOrderLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
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
