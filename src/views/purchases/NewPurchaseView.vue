<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <Form v-slot="{ errors }" @submit="submit()">
      <h2
        class="mb-4 text-2xl font-extrabold tracking-tight leading-none text-gray-700 dark:text-white"
      >
        Seller information:
      </h2>
      <div class="mb-6 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Name</label
          >
          <Field
            required
            :rules="isRequired"
            type="text"
            v-model="seller.sellerName"
            @input="
              $debounce(() => {
                getSellerDetails();
              }, 300)
            "
            placeholder="Seller Name"
            class="default-input w-full"
            :class="errors.sellerName ? 'ring-2 ring-red-500' : ''"
            name="sellerName"
            id="sellerName"
          />
          <span class="text-red-700">{{ errors.sellerName }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Fiscal Number</label
          >
          <Field
            required
            :rules="isRequired"
            type="number"
            step="1"
            v-model="seller.fiscalNumber"
            placeholder="Fiscal Number"
            class="default-input w-full"
            :class="errors.fiscalNumber ? 'ring-2 ring-red-500' : ''"
            name="fiscalNumber"
            id="fiscalNumber"
          />
          <span class="text-red-700">{{ errors.fiscalNumber }}</span>
        </div>
      </div>
      <div class="mb-6 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Invoice Number</label
          >
          <Field
            required
            :rules="isRequired"
            type="text"
            v-model="seller.invoiceNumber"
            placeholder="Invoice Number"
            class="default-input w-full"
            :class="errors.invoiceNumber ? 'ring-2 ring-red-500' : ''"
            name="invoiceNumber"
            id="invoiceNumber"
          />
          <span class="text-red-700">{{ errors.invoiceNumber }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Seller Tax Number</label
          >
          <Field
            required
            :rules="isRequired"
            type="number"
            step="1"
            v-model="seller.taxNumber"
            placeholder="Tax Number"
            class="default-input w-full"
            :class="errors.taxNumber ? 'ring-2 ring-red-500' : ''"
            name="taxNumber"
            id="taxNumber"
          />
          <span class="text-red-700">{{ errors.taxNumber }}</span>
        </div>
      </div>
      <h2
        class="mb-4 mt-7 text-2xl font-extrabold tracking-tight leading-none text-gray-700 dark:text-white"
      >
        Purchased products:
      </h2>
      <div
        v-for="(product, index) in products"
        :key="index"
        class="flex gap-2 mb-6"
      >
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Barcode</label
          >
          <Field
            required
            :rules="isRequired"
            @input="
              $debounce(() => {
                getProductDetails(product.barcode, index);
              }, 300)
            "
            type="number"
            step="1"
            v-model="product.barcode"
            placeholder="Product Barcode"
            class="default-input w-full"
            :class="errors[`${index}barcode`] ? 'ring-2 ring-red-500' : ''"
            :name="`${index}barcode`"
            :id="`${index}barcode`"
          />
          <span class="text-red-700">{{ errors[`${index}barcode`] }}</span>
        </div>
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Name</label
          >
          <Field
            required
            :rules="isRequired"
            type="text"
            v-model="product.productName"
            placeholder="Product Name"
            class="default-input w-full"
            :class="errors[`${index}name`] ? 'ring-2 ring-red-500' : ''"
            :name="`${index}name`"
            :id="`${index}name`"
          />
          <span class="text-red-700">{{ errors[`${index}name`] }}</span>
        </div>
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Stock</label
          >
          <Field
            required
            :rules="isRequired"
            type="number"
            step="1"
            v-model="product.stock"
            placeholder="Product Stock"
            class="default-input w-full"
            :class="errors[`${index}stock`] ? 'ring-2 ring-red-500' : ''"
            :name="`${index}stock`"
            :id="`${index}stock`"
          />
          <span class="text-red-700">{{ errors[`${index}stock`] }}</span>
        </div>
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Tax</label
          >
          <Field
            required
            :rules="isRequired"
            type="number"
            step="1"
            v-model="product.tax"
            placeholder="Product Tax"
            class="default-input w-full"
            :class="errors[`${index}tax`] ? 'ring-2 ring-red-500' : ''"
            :name="`${index}tax`"
            :id="`${index}tax`"
            as="select"
          >
            <option value="8">8%</option>
            <option value="18">18%</option></Field
          >
          <span class="text-red-700">{{ errors[`${index}tax`] }}</span>
        </div>
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Purchased Price</label
          >
          <Field
            required
            :rules="isRequired"
            type="number"
            step="0.01"
            v-model="product.purchasedPrice"
            placeholder="Product Purchased Price"
            class="default-input w-full"
            :class="
              errors[`${index}purchasedPrice`] ? 'ring-2 ring-red-500' : ''
            "
            :name="`${index}purchasedPrice`"
            :id="`${index}purchasedPrice`"
          />
          <span class="text-red-700">{{
            errors[`${index}purchasedPrice`]
          }}</span>
        </div>
        <div class="basis-1/6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >Selling Price</label
          >
          <div class="flex items-center gap-2">
            <Field
              required
              :rules="isRequired"
              type="number"
              step="0.01"
              v-model="product.sellingPrice"
              placeholder="Product Selling Price"
              class="default-input w-full"
              :class="
                errors[`${index}sellingPrice`] ? 'ring-2 ring-red-500' : ''
              "
              :name="`${index}sellingPrice`"
              :id="`${index}sellingPrice`"
            />
            <button
              v-show="products.length != 1"
              type="button"
              class="p-1.5 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-900 items-end mt-auto mb-auto"
              @click="removeProduct(index)"
            >
              <IconC
                iconName="TrashIcon"
                iconClass="w-5 h-5 text-red-700 cursor-pointer"
              />
            </button>
          </div>
          <span class="text-red-700">{{ errors[`${index}sellingPrice`] }}</span>
        </div>
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
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";
export default {
  components: {
    Field,
    Form,
  },
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
    isRequired(value) {
      return value ? true : "This field is required";
    },
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
    getProductDetails(e, idx) {
      this.$store
        .dispatch("productModule/getProductDetailsByBarcode", e)
        .then(async (res) => {
          const options = this.$swalConfirmObject();
          options.position = "top-end";
          options.toast = true;
          options.icon = "info";
          options.timer = 10000;
          options.html =
            "<p class='text-gray-500 dark:text-gray-300'>We found a product with this barcode, do you want to automatically fill the rest of the fields?</p>";
          await this.$swal(options).then((result) => {
            if (result.isConfirmed) {
              const foundProduct = this.products[idx];
              foundProduct.productName = res.data.name;
              foundProduct.tax = res.data.tax;
              foundProduct.sellingPrice = res.data.sellingPrice;
              foundProduct.purchasedPrice = res.data.purchasedPrice;
            }
          });
        })
        .catch(() => console.log());
    },
    getSellerDetails() {
      this.$store
        .dispatch("purchaseModule/getSellerDetails", this.seller.sellerName)
        .then(async (res) => {
          const options = this.$swalConfirmObject();
          options.position = "top-end";
          options.toast = true;
          options.icon = "info";
          options.timer = 10000;
          options.html =
            "<p class='text-gray-500 dark:text-gray-300'>We found a seller with this name, do you want to automatically fill the rest of the informations?</p>";
          await this.$swal(options).then((result) => {
            if (result.isConfirmed) {
              this.seller.fiscalNumber = res.data.sellerFiscalNumber;
              this.seller.taxNumber = res.data.sellerTaxNumber;
            }
          });
        })
        .catch(() => console.log());
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
          this.$router.push({ name: "purchases" });
        })
        .catch(() => {
          this.isLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
  },
};
</script>
