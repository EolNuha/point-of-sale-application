<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <form @submit.prevent="submit()">
      <h2
        class="mb-4 text-2xl font-extrabold tracking-tight leading-none text-gray-900 md:text-3xl dark:text-white"
      >
        Seller information:
      </h2>
      <div class="flex flex-row items-center gap-2 my-2">
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Name</label
          >
          <input
            required
            type="text"
            v-model="seller.sellerName"
            placeholder="Seller Name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Fiscal Number</label
          >
          <input
            required
            type="number"
            step="1"
            v-model="seller.fiscalNumber"
            placeholder="Fiscal Number"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
      </div>
      <div class="flex flex-row items-center gap-2 my-2">
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Invoice Number</label
          >
          <input
            required
            type="text"
            v-model="seller.invoiceNumber"
            placeholder="Invoice Number"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Tax Number</label
          >
          <input
            required
            type="number"
            step="1"
            v-model="seller.taxNumber"
            placeholder="Tax Number"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
      </div>
      <h2
        class="mb-4 mt-7 text-2xl font-extrabold tracking-tight leading-none text-gray-900 md:text-3xl dark:text-white"
      >
        Purchased products:
      </h2>
      <div
        v-for="(product, index) in products"
        :key="product.name"
        class="flex flex-row items-center gap-2 my-2"
      >
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Barcode</label
          >
          <input
            required
            type="number"
            v-model="product.barcode"
            placeholder="Product Barcode"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Name</label
          >
          <input
            required
            type="text"
            v-model="product.productName"
            placeholder="Product Name"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Stock</label
          >
          <input
            required
            type="number"
            step="0.01"
            v-model="product.stock"
            placeholder="Product Stock"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Tax</label
          >
          <select
            v-model="product.tax"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          >
            <option value="8">8%</option>
            <option value="18">18%</option>
          </select>
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Purchased Price</label
          >
          <input
            required
            type="number"
            step="0.01"
            v-model="product.purchasedPrice"
            placeholder="Product Purchased Price"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <div class="w-full">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Selling Price</label
          >
          <input
            required
            type="number"
            step="0.01"
            v-model="product.sellingPrice"
            placeholder="Product Selling Price"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <button
          v-show="products.length != 1"
          type="button"
          class="p-1.5 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-900 items-end mt-auto mb-2"
          @click="removeProduct(index)"
        >
          <IconC
            iconName="TrashIcon"
            iconClass="w-5 h-5 text-red-700 cursor-pointer"
          />
        </button>
      </div>
      <div class="flex justify-end my-3 gap-2">
        <button
          type="button"
          class="blue-gradient-btn flex items-center justify-center"
          @click="addProduct"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5" />
        </button>
      </div>
      <div>
        <button
          type="submit"
          class="blue-gradient-btn w-32 flex justify-center items-center"
        >
          <div role="status" v-if="isLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
            />
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else>Submit</div>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoading: false,
      seller: {
        sellerName: "",
        invoiceNumber: "",
        fiscalNumber: "",
        taxNumber: "",
      },
      products: [
        {
          barcode: "",
          productName: "",
          stock: "",
          tax: 8,
          purchasedPrice: "",
          sellingPrice: "",
        },
      ],
    };
  },
  methods: {
    addProduct() {
      const product = {
        barcode: "",
        productName: "",
        stock: "",
        tax: 8,
        purchasedPrice: "",
        sellingPrice: "",
      };
      this.products.push(product);
    },
    removeProduct(productIdx) {
      this.products.splice(productIdx, 1);
    },
    getProductsTotal() {
      const products = this.products;
      const sum = products.reduce((accumulator, object) => {
        return accumulator + object.purchasedPrice * object.stock;
      }, 0);
      return sum.toFixed(2);
    },
    submit() {
      this.isLoading = true;
      const data = {
        products: this.products,
        seller: this.seller,
        totalAmount: this.getProductsTotal(),
      };
      this.$store
        .dispatch("purchaseModule/createPurchase", data)
        .then(() => {
          this.isLoading = false;
          this.seller = {
            sellerName: "",
            invoiceNumber: "",
            fiscalNumber: "",
            taxNumber: "",
          };
          this.products = [
            {
              barcode: "",
              productName: "",
              stock: "",
              tax: 8,
              purchasedPrice: "",
              sellingPrice: "",
            },
          ];
          this.$toast.success("Purchase saved successfully!");
        })
        .catch(() => {
          this.isLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
  },
};
</script>
