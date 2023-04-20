<template>
  <div
    class="flex flex-col bg-neutral-200 dark:bg-neutral-800 min-h-screen relative"
  >
    <OverlayC
      v-if="isDataLoading"
      :outerDiv="`opacity-[95] bg-neutral-100 dark:bg-neutral-900 `"
    />
    <Form
      v-slot="{ errors }"
      class="p-5"
      @submit="isAdd ? createProduct() : updateProduct()"
    >
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_name"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("productName") }}</label
          >
          <Field
            name="product_name"
            rules="required"
            v-model="product.name"
            type="text"
            id="product_name"
            class="default-input w-full"
            placeholder="Enter product name"
            required
          />
          <span class="text-red-700">{{ errors.product_name }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_barcode"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("barcode") }}</label
          >
          <Field
            name="product_barcode"
            rules="required"
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
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_measure"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("measure") }}</label
          >
          <Field
            type="text"
            v-model="product.measure"
            class="hidden"
            name="product_measure"
            id="product_measure"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.product_measure ? 'ring-2 ring-red-500' : ''"
            v-model="product.measure"
            :clearable="false"
            :options="measures"
            :reduce="(t) => t.settingsValue"
            :label="`settingsValue`"
            type="text"
            :placeholder="$t('measure')"
          >
            <template v-slot:option="option">
              {{ $t(option.settingsValue) }}
            </template>
            <template v-slot:selected-option="option">
              {{ $t(option.settingsValue) }}
            </template>
          </v-select>
          <span class="text-red-700">{{ errors.product_measure }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_stock"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("stock") }}</label
          >
          <Field
            name="product_stock"
            rules="required"
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
            for="product_purchased_price_wo_tax"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchasedPriceWOTax") }}</label
          >
          <Field
            name="product_purchased_price_wo_tax"
            rules="required"
            v-model="product.purchasedPriceWOTax"
            type="number"
            id="product_purchased_price_wo_tax"
            :class="
              errors.product_purchased_price_wo_tax ? 'ring-2 ring-red-500' : ''
            "
            class="default-input w-full"
            placeholder="Enter product purchased price w/o tax"
            required
          />
          <span class="text-red-700">{{
            errors.product_purchased_price_wo_tax
          }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_purchasedprice"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchasedPrice") }}</label
          >
          <Field
            name="product_purchasedprice"
            rules="required"
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
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_sellingprice"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("sellingPrice") }}</label
          >
          <Field
            name="product_sellingprice"
            rules="required"
            v-model="product.sellingPrice"
            type="number"
            step="0.01"
            id="product_sellingprice"
            class="default-input w-full"
            placeholder="Enter product selling price"
            required
          />
          <span class="text-red-700">{{ errors.product_sellingprice }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_tax"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("tax") }}</label
          >
          <Field
            type="text"
            v-model="product.tax"
            class="hidden"
            name="product_tax"
            id="product_tax"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.product_tax ? 'ring-2 ring-red-500' : ''"
            v-model="product.tax"
            :clearable="false"
            :options="taxes"
            :reduce="(t) => t.settingsValue"
            :label="`settingsValue`"
            type="text"
            :placeholder="$t('tax')"
          >
            <template v-slot:option="option">
              {{ option.settingsValue }}%
            </template>
            <template v-slot:selected-option="option">
              {{ option.settingsValue }}%
            </template>
          </v-select>
          <span class="text-red-700">{{ errors.product_tax }}</span>
        </div>
      </div>
      <div class="mb-6 flex gap-4">
        <div class="basis-1/2">
          <label
            for="product_expire"
            class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("expirationDate") }}
            <button
              :id="`product-exp-tooltip-btn`"
              class="cursor-default"
              type="button"
              @mouseover="
                $showTooltip({
                  targetEl: `product-exp-tooltip`,
                  triggerEl: `product-exp-tooltip-btn`,
                  placement: `right`,
                })
              "
            >
              <IconC iconName="InformationCircleIcon" iconClass="w-4 h-4" />
            </button>
            <div
              :id="`product-exp-tooltip`"
              role="tooltip"
              class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 dark:bg-neutral-900 rounded shadow-sm opacity-0 tooltip max-w-[250px]"
            >
              {{ $t("expirationFieldEmptyMsg") }}
            </div>
          </label>
          <Field
            name="product_expire"
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
        <div class="basis-1/2" v-if="!isAdd">
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
      </div>
      <div class="mb-6 flex gap-4" v-if="!isAdd">
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
        class="theme-gradient-btn w-32 flex justify-center items-center"
      >
        <div role="status" v-if="isUpdateLoading">
          <IconC
            iconType="custom"
            iconName="SpinnerIcon"
            iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
          />
          <span class="sr-only">Loading...</span>
        </div>
        <div v-else>{{ isAdd ? "Submit" : $t("update") }}</div>
      </button>
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";
import Product from "@/models/product";
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
      measures: [],
      isAdd: true,
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
      const t = JSON.parse(
        JSON.stringify(this.$store.state.settingsModule.settingsType)
      );
      t.unshift({
        settingsValue: 0,
      });
      return t;
    },
    minDate() {
      return this.formatDate(new Date());
    },
  },
  async created() {
    await this.reload();
  },
  unmounted() {
    this.$store.state.productModule.product = new Product();
  },
  methods: {
    async reload() {
      this.isDataLoading = true;
      await this.$store
        .dispatch("settingsModule/getSettingsType", {
          settingsType: "measure",
        })
        .then((response) => {
          this.measures = response.data;
        });
      await this.$store.dispatch("settingsModule/getSettingsType", {
        settingsType: "tax",
      });
      if (this.$route.params.productId) {
        this.isAdd = false;
        await this.$store
          .dispatch(
            "productModule/getProductDetails",
            this.$route.params.productId
          )
          .then(async (response) => {
            this.$route.meta.title = response.data.name;
            this.isDataLoading = false;
            document.title = this.product.name;
          });
      }
      this.isDataLoading = false;
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
    updateProduct() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("productModule/updateProduct", this.product)
        .then(() => {
          this.isUpdateLoading = false;
          this.$toast.success(this.$t("productUpdatedSuccessfully"));
        })
        .catch((error) => {
          this.isUpdateLoading = false;
          this.$toast.error(
            this.$t(error.response.data) || this.$t("somethingWrong")
          );
        });
    },
    createProduct() {
      this.isUpdateLoading = true;
      this.$store
        .dispatch("productModule/createProduct", this.product)
        .then(() => {
          this.isUpdateLoading = false;
          this.$router.push({
            name: "products",
          });
          this.$toast.success(this.$t("productCreatedSuccessfully"));
        })
        .catch((error) => {
          this.isUpdateLoading = false;
          this.$toast.error(
            this.$t(error.response.data) || this.$t("somethingWrong")
          );
        });
    },
  },
};
</script>
