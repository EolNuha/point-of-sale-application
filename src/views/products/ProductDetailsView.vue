<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen relative">
    <OverlayC v-if="isDataLoading" />
    <Form v-slot="{ errors }" class="p-5" @submit="updateProduct">
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
            for="product_stock"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("tax") }}</label
          >
          <Field
            name="product_tax"
            :rules="isRequired"
            v-model="product.tax"
            id="product_tax"
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
            :placeholder="$t('expirationDate')"
            required
          />
          <span class="text-red-700">{{ errors.product_expire }}</span>
        </div>
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="dateCreated"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("dateCreated") }}</label
          >
          <input
            name="product_price"
            v-model="product.dateCreated"
            type="text"
            id="dateCreated"
            class="default-input w-full"
            placeholder="Enter product price"
            disabled
          />
        </div>
        <div class="basis-1/2">
          <label
            for="dateModified"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("dateModified") }}</label
          >
          <input
            name="dateModified"
            v-model="product.dateModified"
            type="text"
            id="dateModified"
            class="default-input w-full"
            disabled
          />
        </div>
      </div>
      <button
        type="submit"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-32 px-5 py-1.5 flex justify-center items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <div role="status" v-if="isUpdateLoading">
          <IconC
            iconType="custom"
            iconName="SpinnerIcon"
            iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
          />
          <span class="sr-only">Loading...</span>
        </div>
        <div v-else>{{ $t("update") }}</div>
      </button>
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";

export default {
  name: "ProductDetailsView",
  components: {
    Field,
    Form,
  },
  data() {
    return {
      isDataLoading: true,
      isUpdateLoading: false,
    };
  },
  watch: {
    "$route.params.productId": {
      handler: function () {
        this.reload();
      },
      deep: true,
      immediate: true,
    },
    "$route.query.notificationId": {
      handler: function (value) {
        if (value) {
          this.$store.dispatch("notificationsModule/updateNotification", {
            id: value,
            read: true,
            star: null,
          });
        }
      },
      deep: true,
      immediate: true,
    },
  },
  computed: {
    product() {
      return this.$store.state.productModule.product;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
    minDate() {
      return this.formatDate(new Date());
    },
  },
  async created() {
    this.reload();
  },
  methods: {
    reload() {
      this.isDataLoading = true;
      this.$store.dispatch("settingsModule/getSettingsType", {
        settingsType: "tax",
      });
      this.$store
        .dispatch(
          "productModule/getProductDetails",
          this.$route.params.productId
        )
        .then(async (response) => {
          this.$route.meta.title = response.data.name;
          this.isDataLoading = false;
        });
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
    isRequired(value) {
      return value ? true : this.$t("isRequired");
    },
    updateProduct() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("productModule/updateProduct", this.product)
        .then(() => {
          this.isUpdateLoading = false;
          this.$toast.success(this.$t("productUpdatedSuccessfully"));
        })
        .catch(() => {
          this.isUpdateLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
  },
};
</script>
