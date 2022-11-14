<template>
  <div class="bg-gray-200 dark:bg-neutral-800 min-h-screen">
    <Form v-slot="{ errors }" class="p-5" @submit="createProduct">
      <div class="mb-6">
        <label
          for="product_name"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
          >{{ $t("productName") }}</label
        >
        <Field
          name="product_name"
          :rules="isRequired"
          v-model="product.name"
          type="text"
          id="product_name"
          :class="errors.product_name ? 'ring-2 ring-red-500' : ''"
          class="default-input w-full"
          placeholder="Enter product name"
          required
        />
        <span class="text-red-700">{{ errors.product_name }}</span>
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_barcode"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("barcode") }}</label
          >
          <Field
            name="product_barcode"
            :rules="isRequired"
            v-model="product.barcode"
            type="number"
            id="product_barcode"
            :class="errors.product_barcode ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product barcode"
            required
          />
          <span class="text-red-700">{{ errors.product_barcode }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_stock"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("stock") }}</label
          >
          <Field
            name="product_stock"
            :rules="isRequired"
            v-model="product.stock"
            type="number"
            id="product_stock"
            :class="errors.product_stock ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product stock"
            required
          />
          <span class="text-red-700">{{ errors.product_stock }}</span>
        </div>
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_purchasedprice"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchasedPrice") }}</label
          >
          <Field
            name="product_purchasedprice"
            :rules="isRequired"
            v-model="product.purchasedPrice"
            type="number"
            step="0.01"
            id="product_purchasedprice"
            :class="errors.product_purchasedprice ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product price"
            required
          />
          <span class="text-red-700">{{ errors.product_purchasedprice }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_sellingprice"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("sellingPrice") }}</label
          >
          <Field
            name="product_sellingprice"
            :rules="isRequired"
            v-model="product.sellingPrice"
            type="number"
            step="0.01"
            id="product_sellingprice"
            :class="errors.product_sellingprice ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product price"
            required
          />
          <span class="text-red-700">{{ errors.product_sellingprice }}</span>
        </div>
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_tax"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("tax") }}</label
          >
          <Field
            name="product_tax"
            :rules="isRequired"
            v-model="product.tax"
            id="product_tax"
            :class="errors.product_tax ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            required
            as="select"
          >
            <option
              v-for="item in taxes"
              :key="item.settingsValue"
              :value="item.settingsValue"
            >
              {{ item.settingsName }}%
            </option>
          </Field>
          <span class="text-red-700">{{ errors.product_tax }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_expire"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("expirationDate") }}</label
          >
          <Field
            name="product_expire"
            :rules="isRequired"
            v-model="product.expirationDate"
            :min="minDate"
            type="date"
            id="product_expire"
            :class="errors.product_expire ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product stock"
            required
          />
          <span class="text-red-700">{{ errors.product_expire }}</span>
        </div>
      </div>

      <button
        type="submit"
        class="theme-gradient-btn w-32 flex justify-center items-center"
      >
        <div role="status" v-if="isLoading">
          <IconC
            iconType="custom"
            iconName="SpinnerIcon"
            iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
          />
          <span class="sr-only">Loading...</span>
        </div>
        <div v-else>Submit</div>
      </button>
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";

export default {
  name: "CreateProductView",
  components: {
    Field,
    Form,
  },
  data() {
    return {
      product: {
        name: "",
        barcode: "",
        stock: "",
        expirationDate: "",
        tax: 8,
        purchasedPrice: "",
        sellingPrice: "",
      },
      isLoading: false,
    };
  },
  computed: {
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
    minDate() {
      return this.formatDate(new Date());
    },
  },
  async created() {
    await this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
  },
  methods: {
    isRequired(value) {
      return value ? true : this.$t("isRequired");
    },
    formatDate(date) {
      return (
        String(date.getFullYear()).padStart(2, "0") +
        "-" +
        String(date.getMonth() + 1).padStart(2, "0") +
        "-" +
        String(date.getDate()).padStart(2, "0")
      );
    },
    createProduct() {
      this.isLoading = true;
      this.$store
        .dispatch("productModule/createProduct", this.product)
        .then(() => {
          this.isLoading = false;
          this.$router.push({
            name: "products",
          });
          this.$toast.success(this.$t("productCreatedSuccessfully"));
        })
        .catch((error) => {
          this.isLoading = false;
          this.$toast.error(
            this.$t(error.response.data) || this.$t("somethingWrong")
          );
        });
    },
  },
};
</script>
