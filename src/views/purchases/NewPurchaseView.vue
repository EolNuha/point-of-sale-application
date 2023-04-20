<template>
  <div class="main-div">
    <Form v-slot="{ errors }" @submit="submit()">
      <h2
        class="mb-4 text-2xl font-extrabold tracking-tight leading-none text-gray-700 dark:text-white"
      >
        {{ $t("sellerInfo") }}:
      </h2>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("sellerName") }}</label
          >
          <Field
            required
            rules="required"
            type="text"
            v-model="seller.sellerName"
            class="hidden"
            name="sellerName"
            id="sellerName"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.sellerName ? 'ring-2 ring-red-500' : ''"
            v-model="seller.sellerName"
            @search="($event, loading) => searchSellers($event, loading)"
            @close="seller.search ? getSellerDetails(seller.search) : ''"
            :clearable="true"
            :filterable="false"
            :options="sellers"
            :reduce="(sellers) => sellers.sellerName"
            label="sellerName"
            type="text"
            :placeholder="$t('sellerName')"
            :taggable="true"
            @option:selected="getSellerDetails($event)"
          />
          <span class="text-red-700">{{ errors.sellerName }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("fiscalNumber") }}:</label
          >
          <Field
            required
            rules="required"
            type="number"
            step="1"
            v-model="seller.fiscalNumber"
            :placeholder="$t('fiscalNumber')"
            class="default-input w-full"
            :class="errors.fiscalNumber ? 'ring-2 ring-red-500' : ''"
            name="fiscalNumber"
            id="fiscalNumber"
          />
          <span class="text-red-700">{{ errors.fiscalNumber }}</span>
        </div>
      </div>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("taxNumber") }}</label
          >
          <Field
            required
            rules="required"
            type="number"
            step="1"
            v-model="seller.taxNumber"
            :placeholder="$t('taxNumber')"
            class="default-input w-full"
            :class="errors.taxNumber ? 'ring-2 ring-red-500' : ''"
            name="taxNumber"
            id="taxNumber"
          />
          <span class="text-red-700">{{ errors.taxNumber }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("invoiceNumber") }}</label
          >
          <Field
            required
            rules="required"
            type="text"
            v-model="seller.invoiceNumber"
            :placeholder="$t('invoiceNumber')"
            class="default-input w-full"
            :class="errors.invoiceNumber ? 'ring-2 ring-red-500' : ''"
            name="invoiceNumber"
            id="invoiceNumber"
          />
          <span class="text-red-700">{{ errors.invoiceNumber }}</span>
        </div>
      </div>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchaseDate") }}</label
          >
          <Field
            required
            rules="required"
            type="date"
            v-model="seller.purchaseDate"
            :placeholder="$t('purchaseDate')"
            class="default-input w-full"
            :class="errors.purchaseDate ? 'ring-2 ring-red-500' : ''"
            name="purchaseDate"
            id="purchaseDate"
          />
          <span class="text-red-700">{{ errors.purchaseDate }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchaseType") }}</label
          >
          <Field
            required
            rules="required"
            type="number"
            step="1"
            v-model="seller.purchaseType"
            class="hidden"
            :name="`purchaseType`"
            :id="`purchaseType`"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.purchaseType ? 'ring-2 ring-red-500' : ''"
            v-model="seller.purchaseType"
            :options="purchaseTypes"
            :reduce="(t) => t.settingsValue"
            :label="`settingsValue`"
            :clearable="false"
            type="text"
            :placeholder="$t('purchaseType')"
          >
            <template v-slot:option="option">
              {{ $t(option.settingsValue) }}
            </template>
            <template v-slot:selected-option="option">
              {{ $t(option.settingsValue) }}
            </template>
          </v-select>
          <span class="text-red-700">{{ errors.purchaseType }}</span>
        </div>
      </div>
      <h2
        class="mb-0 mt-7 text-2xl font-extrabold tracking-tight leading-none text-gray-700 dark:text-white"
      >
        {{ $t("purchasedProducts") }}:
      </h2>
      <div class="divide-y divide-gray-400">
        <div v-for="(product, index) in products" :key="index" class="py-5">
          <div class="flex flex-row gap-2">
            <div
              class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 w-full"
            >
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("barcode") }}</label
                >
                <Field
                  required
                  rules="required"
                  type="number"
                  step="1"
                  v-model="product.barcode"
                  :placeholder="$t('barcode')"
                  class="hidden"
                  :name="`${index}barcode`"
                  :id="`${index}barcode`"
                />
                <v-select
                  class="block w-full default-input !p-[1px]"
                  :class="
                    errors[`${index}barcode`] ? 'ring-2 ring-red-500' : ''
                  "
                  v-model="product.barcode"
                  @search="
                    ($event, loading) =>
                      searchProducts($event, loading, index, 'barcode')
                  "
                  @close="
                    product.search
                      ? getProductDetailsBarcode(product.search, index)
                      : ''
                  "
                  :clearable="true"
                  :filterable="false"
                  :options="productsList"
                  :reduce="(productsList) => productsList.barcode"
                  label="barcode"
                  type="text"
                  :placeholder="$t('barcode')"
                  :taggable="true"
                  @option:selected="getProductDetailsBarcode($event, index)"
                />
                <span class="text-red-700">{{
                  errors[`${index}barcode`]
                }}</span>
              </div>
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("productName") }}</label
                >
                <Field
                  required
                  rules="required"
                  type="text"
                  v-model="product.productName"
                  :placeholder="$t('productName')"
                  class="hidden"
                  :name="`${index}name`"
                  :id="`${index}name`"
                />
                <v-select
                  class="block w-full default-input !p-[1px]"
                  :class="errors[`${index}name`] ? 'ring-2 ring-red-500' : ''"
                  v-model="product.productName"
                  @search="
                    ($event, loading) =>
                      searchProducts($event, loading, index, 'name')
                  "
                  @close="
                    product.search
                      ? getProductDetails(product.search, index)
                      : ''
                  "
                  :clearable="true"
                  :filterable="false"
                  :options="productsList"
                  :reduce="(productsList) => productsList.name"
                  label="name"
                  type="text"
                  :placeholder="$t('productName')"
                  :taggable="true"
                  @option:selected="getProductDetails($event, index)"
                />
                <span class="text-red-700">{{ errors[`${index}name`] }}</span>
              </div>
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("measure") }}</label
                >
                <Field
                  type="text"
                  v-model="product.measure"
                  class="hidden"
                  :name="`${index}measure`"
                  :id="`${index}measure`"
                />
                <v-select
                  class="block w-full default-input !p-[1px]"
                  :class="
                    errors[`${index}measure`] ? 'ring-2 ring-red-500' : ''
                  "
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
                <span class="text-red-700">{{
                  errors[`${index}measure`]
                }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("stock") }}
                  <button
                    :id="`product-${index}-tooltip-btn`"
                    class="cursor-default"
                    type="button"
                    @mouseover="
                      $showTooltip({
                        targetEl: `product-${index}-tooltip`,
                        triggerEl: `product-${index}-tooltip-btn`,
                        placement: `right`,
                      })
                    "
                  >
                    <IconC
                      iconName="InformationCircleIcon"
                      iconClass="w-4 h-4"
                    />
                  </button>
                  <div
                    :id="`product-${index}-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 dark:bg-neutral-900 rounded shadow-sm opacity-0 tooltip max-w-[250px]"
                  >
                    {{ $t("stockInfoMsg") }}
                  </div>
                </label>
                <div class="flex items-center gap-2">
                  <Field
                    required
                    rules="required"
                    type="number"
                    v-model="product.stock"
                    :placeholder="$t('stock')"
                    class="default-input w-full"
                    :class="
                      errors[`${index}stock`] ? 'ring-2 ring-red-500' : ''
                    "
                    :name="`${index}stock`"
                    :id="`${index}stock`"
                  />
                </div>
                <span class="text-red-700">{{ errors[`${index}stock`] }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("purchasedPrice") }}
                  <button
                    :id="`purchased-${index}-tooltip-btn`"
                    class="cursor-default"
                    type="button"
                    @mouseover="
                      $showTooltip({
                        targetEl: `purchased-${index}-tooltip`,
                        triggerEl: `purchased-${index}-tooltip-btn`,
                        placement: `right`,
                      })
                    "
                  >
                    <IconC
                      iconName="InformationCircleIcon"
                      iconClass="w-4 h-4"
                    />
                  </button>
                  <div
                    :id="`purchased-${index}-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 dark:bg-neutral-900 rounded shadow-sm opacity-0 tooltip max-w-[250px]"
                  >
                    {{ $t("purchasedPrice") }} {{ $t("withoutTax") }}
                  </div>
                </label>
                <Field
                  required
                  rules="required"
                  type="number"
                  step="0.01"
                  v-model="product.purchasedPrice"
                  :placeholder="`${$t('purchasedPrice')} (${$t('withoutTax')})`"
                  class="default-input w-full"
                  :class="
                    errors[`${index}purchasedPrice`]
                      ? 'ring-2 ring-red-500'
                      : ''
                  "
                  :name="`${index}purchasedPrice`"
                  :id="`${index}purchasedPrice`"
                />
                <span class="text-red-700">{{
                  errors[`${index}purchasedPrice`]
                }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("rabat") }} (%)
                </label>
                <Field
                  required
                  rules="required|minMax:0,100"
                  type="number"
                  step="0.01"
                  v-model="product.rabat"
                  :placeholder="$t('rabat')"
                  class="default-input w-full"
                  :class="errors[`${index}rabat`] ? 'ring-2 ring-red-500' : ''"
                  :name="`${index}rabat`"
                  :id="`${index}rabat`"
                />
                <span class="text-red-700">{{ errors[`${index}rabat`] }}</span>
              </div>
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("tax") }}</label
                >
                <Field
                  type="number"
                  v-model="product.tax"
                  class="hidden"
                  :name="`${index}tax`"
                  :id="`${index}tax`"
                />
                <v-select
                  class="block w-full default-input !p-[1px]"
                  :class="errors[`${index}tax`] ? 'ring-2 ring-red-500' : ''"
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
                <span class="text-red-700">{{ errors[`${index}tax`] }}</span>
              </div>
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("sellingPrice") }}</label
                >
                <Field
                  required
                  rules="required"
                  type="number"
                  step="0.01"
                  v-model="product.sellingPrice"
                  :placeholder="$t('sellingPrice')"
                  class="default-input w-full"
                  :class="
                    errors[`${index}sellingPrice`] ? 'ring-2 ring-red-500' : ''
                  "
                  :name="`${index}sellingPrice`"
                  :id="`${index}sellingPrice`"
                />
                <span class="text-red-700">{{
                  errors[`${index}sellingPrice`]
                }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("expirationDate") }}
                  <button
                    :id="`product-exp-${index}-tooltip-btn`"
                    class="cursor-default"
                    type="button"
                    @mouseover="
                      $showTooltip({
                        targetEl: `product-exp-${index}-tooltip`,
                        triggerEl: `product-exp-${index}-tooltip-btn`,
                        placement: `right`,
                      })
                    "
                  >
                    <IconC
                      iconName="InformationCircleIcon"
                      iconClass="w-4 h-4"
                    />
                  </button>
                  <div
                    :id="`product-exp-${index}-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 dark:bg-neutral-900 rounded shadow-sm opacity-0 tooltip max-w-[250px]"
                  >
                    {{ $t("expirationFieldEmptyMsg") }}
                  </div>
                </label>
                <Field
                  :name="`${index}product_expire`"
                  :id="`${index}product_expire`"
                  v-model="product.expirationDate"
                  :min="minDate"
                  type="date"
                  :class="
                    errors[`${index}product_expire`]
                      ? 'ring-2 ring-red-500'
                      : ''
                  "
                  class="default-input w-full"
                  :placeholder="$t('expirationDate')"
                  required
                />
                <span class="text-red-700">{{
                  errors[`${index}product_expire`]
                }}</span>
              </div>
            </div>
            <button
              v-show="products?.length != 1"
              type="button"
              class="p-1.5 rounded hover:bg-neutral-300/50 dark:hover:bg-neutral-900/50"
              @click="removeProduct(index)"
            >
              <IconC
                iconName="TrashIcon"
                iconClass="w-5 h-5 text-red-700 cursor-pointer"
              />
            </button>
          </div>
        </div>
      </div>
      <div class="flex justify-end my-3 gap-2">
        <button
          type="button"
          class="theme-gradient-btn flex items-center justify-center"
          @click="addProduct"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5" />
        </button>
      </div>
      <div>
        <button
          type="submit"
          class="theme-gradient-btn w-32 flex justify-center items-center"
          :disabled="isLoading"
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
  setup() {},
  data() {
    return {
      isLoading: false,
      measures: [],
      purchaseTypes: [],
      seller: {
        sellerName: "",
        invoiceNumber: "",
        fiscalNumber: "",
        taxNumber: "",
        purchaseDate: new Date(),
        purchaseType: "purchase",
        search: "",
      },
      products: [
        {
          barcode: null,
          productName: "",
          stock: null,
          tax: 0,
          rabat: "0",
          purchasedPrice: null,
          sellingPrice: null,
          measure: "pcs",
          expirationDate: "",
          search: "",
        },
      ],
    };
  },
  computed: {
    productsList() {
      return this.$store.getters["productModule/getProductsList"];
    },
    sellers() {
      return this.$store.getters["purchaseModule/getSellersList"];
    },
    minDate() {
      return this.formatDate(new Date());
    },
    taxes() {
      const t = JSON.parse(
        JSON.stringify(this.$store.state.settingsModule.settingsType)
      );
      t.unshift({
        settingsName: "0",
        settingsAlias: "zero",
        settingsType: "tax",
        settingsValue: 0,
      });
      return t;
    },
  },
  async created() {
    this.seller.purchaseDate = this.minDate;
    await this.$store
      .dispatch("settingsModule/getSettingsType", {
        settingsType: "measure",
      })
      .then((response) => {
        this.measures = response.data;
      });
    await this.$store
      .dispatch("settingsModule/getSettingsType", {
        settingsType: "purchasetype",
      })
      .then((response) => {
        this.purchaseTypes = response.data;
      });
    await this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.getSellers("");
    await this.getProducts("");
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
    addProduct() {
      const product = {
        barcode: null,
        productName: "",
        stock: null,
        tax: 0,
        rabat: "0",
        purchasedPrice: null,
        sellingPrice: null,
        measure: "pcs",
        expirationDate: "",
        search: "",
      };
      this.products.push(product);
    },
    removeProduct(productIdx) {
      this.products.splice(productIdx, 1);
    },
    async searchSellers(search, loading) {
      this.seller.search = search;
      loading(true);
      await this.getSellers(search);
      loading(false);
    },
    async getSellers(search) {
      await this.$store.dispatch("purchaseModule/getSellers", {
        page: 1,
        per_page: 20,
        sort_column: "seller_name",
        sort_dir: "asc",
        search: search,
      });
    },
    getSellerDetails(e) {
      const sellerName = e.sellerName ? e.sellerName : e;
      this.seller.sellerName = sellerName;
      const sellerInfo = this.sellers.find(
        (x) => x.sellerName.toLowerCase() === sellerName.toLowerCase()
      );
      if (sellerInfo) {
        this.seller.fiscalNumber = sellerInfo?.sellerFiscalNumber;
        this.seller.taxNumber = sellerInfo?.sellerTaxNumber;
      }
    },
    async searchProducts(search, loading, idx, type = "barcode") {
      this.products[idx].search = search;
      loading(true);
      await this.getProducts(search, type);
      loading(false);
    },
    async getProducts(search, type = "barcode") {
      await this.$store.dispatch("productModule/getProducts", {
        page: 1,
        per_page: 20,
        sort_column: type,
        sort_dir: "asc",
        search: search,
      });
    },
    getProductDetails(e, idx) {
      const productName = e.name ? e.name : e;
      this.products[idx].productName = productName;
      const productInfo = this.productsList.find(
        (x) => x.name?.toLowerCase() === productName.toLowerCase()
      );
      if (productInfo) {
        this.products[idx].barcode = productInfo.barcode;
        this.products[idx].tax = productInfo.tax;
        this.products[idx].sellingPrice = productInfo.sellingPrice;
        this.products[idx].purchasedPrice = productInfo.purchasedPriceWOTax;
        this.products[idx].expirationDate = productInfo.expirationDate;
        this.products[idx].measure = productInfo.measure;
      }
    },
    getProductDetailsBarcode(e, idx) {
      const barcode = e.barcode ? e.barcode : e;
      this.products[idx].barcode = barcode;
      const productInfo = this.productsList.find((x) => x.barcode === barcode);
      if (productInfo) {
        this.products[idx].productName = productInfo.name;
        this.products[idx].tax = productInfo.tax;
        this.products[idx].sellingPrice = productInfo.sellingPrice;
        this.products[idx].purchasedPrice = productInfo.purchasedPriceWOTax;
        this.products[idx].expirationDate = productInfo.expirationDate;
        this.products[idx].measure = productInfo.measure;
      }
    },
    submit() {
      this.isLoading = true;
      const data = {
        products: this.products,
        seller: this.seller,
      };
      this.$store
        .dispatch("purchaseModule/createPurchase", data)
        .then(() => {
          this.$router.push({ name: "purchases" });
          this.isLoading = false;
          this.$toast.success(this.$t("purchaseSaved"));
        })
        .catch((err) => {
          const error = err.response.data;
          this.isLoading = false;
          this.$toast.error(
            this.$t(error.message, {
              barcode: error.barcode,
              product: error.product,
            }) || this.$t("somethingWrong")
          );
        });
    },
  },
};
</script>
