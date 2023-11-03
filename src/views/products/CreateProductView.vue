<template>
  <div class="bg-neutral-200 dark:bg-neutral-800 min-h-screen">
    <Form v-slot="{ errors }" class="p-5" @submit="createProduct">
      <div class="mb-6">
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
            for="product_purchased_price"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("_p") }}</label
          >
          <Field
            name="product_purchased_price"
            rules="required"
            v-model="product.purchased_price"
            type="number"
            step="0.01"
            id="product_purchased_price"
            :class="errors.product_purchased_price ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product price"
            required
          />
          <span class="text-red-700">{{ errors.product_purchased_price }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_selling_price"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("selling_price") }}</label
          >
          <Field
            name="product_selling_price"
            rules="required"
            v-model="product.selling_price"
            type="number"
            step="0.01"
            id="product_selling_price"
            :class="errors.product_selling_price ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Enter product price"
            required
          />
          <span class="text-red-700">{{ errors.product_selling_price }}</span>
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
            :reduce="(t) => t.settings_value"
            :label="`settings_value`"
            type="text"
            :placeholder="$t('tax')"
          >
            <template v-slot:option="option">
              {{ option.settings_value }}%
            </template>
            <template v-slot:selected-option="option">
              {{ option.settings_value }}%
            </template>
          </v-select>
          <span class="text-red-700">{{ errors.product_tax }}</span>
        </div>
        <div class="basis-1/2">
          <label
            for="product_expire"
            class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("expiration_date") }}
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
            v-model="product.expiration_date"
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
      isLoading: false,
    };
  },
  computed: {
    taxes() {
      const t = this.$store.state.settingsModule.settings_type;
      t.unshift({
        settings_value: 0,
      });
      return t;
    },
    minDate() {
      return this.formatDate(new Date());
    },
    product: {
      get() {
        return this.$store.state.productModule.product;
      },
      set(v) {
        this.$store.state.productModule.product = v;
      },
    },
  },
  async created() {
    await this.$store.dispatch("settingsModule/getSettingsType", {
      settings_type: "tax",
    });
  },
  methods: {
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
