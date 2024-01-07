<template>
  <div class="main-div">
    <Form v-slot="{ errors }" @submit="submit()" @keydown.enter.prevent>
      <h2
        class="mb-4 text-2xl font-extrabold tracking-tight leading-none text-gray-700 dark:text-white"
      >
        {{ $t("sellerInfo") }}:
      </h2>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("seller_name") }}</label
          >
          <Field
            required
            rules="required"
            type="text"
            v-model="seller.seller_name"
            class="hidden"
            name="seller_name"
            id="seller_name"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.seller_name ? 'ring-2 ring-red-500' : ''"
            v-model="seller.seller_name"
            @search="
              ($event, loading) =>
                $debounce(() => searchSellers($event, loading))
            "
            @close="seller.search ? getSellerDetails(seller.search) : ''"
            :clearable="true"
            :filterable="false"
            :options="sellers"
            :reduce="(sellers) => sellers.seller_name"
            label="seller_name"
            type="text"
            :placeholder="$t('seller_name')"
            :taggable="true"
            @option:selected="getSellerDetails($event)"
          />
          <span class="text-red-700">{{ errors.seller_name }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("fiscal_number") }}:</label
          >
          <Field
            required
            rules="required"
            type="number"
            step="1"
            v-model="seller.fiscal_number"
            :placeholder="$t('fiscal_number')"
            class="default-input w-full"
            :class="errors.fiscal_number ? 'ring-2 ring-red-500' : ''"
            name="fiscal_number"
            id="fiscal_number"
          />
          <span class="text-red-700">{{ errors.fiscal_number }}</span>
        </div>
      </div>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("tax_number") }}</label
          >
          <Field
            type="number"
            step="1"
            v-model="seller.tax_number"
            :placeholder="$t('tax_number')"
            class="default-input w-full"
            :class="errors.tax_number ? 'ring-2 ring-red-500' : ''"
            name="tax_number"
            id="tax_number"
          />
          <span class="text-red-700">{{ errors.tax_number }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("invoice_number") }}</label
          >
          <Field
            required
            rules="required"
            type="text"
            v-model="seller.invoice_number"
            :placeholder="$t('invoice_number')"
            class="default-input w-full"
            :class="errors.invoice_number ? 'ring-2 ring-red-500' : ''"
            name="invoice_number"
            id="invoice_number"
          />
          <span class="text-red-700">{{ errors.invoice_number }}</span>
        </div>
      </div>
      <div class="mb-3 flex gap-2">
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchase_date") }}</label
          >
          <Field
            required
            rules="required"
            type="date"
            v-model="seller.purchase_date"
            :placeholder="$t('purchase_date')"
            class="default-input w-full"
            :class="errors.purchase_date ? 'ring-2 ring-red-500' : ''"
            name="purchase_date"
            id="purchase_date"
          />
          <span class="text-red-700">{{ errors.purchase_date }}</span>
        </div>
        <div class="basis-1/2">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
            >{{ $t("purchase_type") }}</label
          >
          <Field
            required
            rules="required"
            type="number"
            step="1"
            v-model="seller.purchase_type"
            class="hidden"
            :name="`purchase_type`"
            :id="`purchase_type`"
          />
          <v-select
            class="block w-full default-input !p-[1px]"
            :class="errors.purchase_type ? 'ring-2 ring-red-500' : ''"
            v-model="seller.purchase_type"
            :options="purchase_types"
            :reduce="(t) => t.settings_value"
            :label="`settings_value`"
            :clearable="false"
            type="text"
            :placeholder="$t('purchase_type')"
          >
            <template v-slot:option="option">
              {{ $t(option.settings_value) }}
            </template>
            <template v-slot:selected-option="option">
              {{ $t(option.settings_value) }}
            </template>
          </v-select>
          <span class="text-red-700">{{ errors.purchase_type }}</span>
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
              class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2 w-full"
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
                  @click="activeIdx = index"
                  v-model="product.barcode"
                  @search="
                    ($event, loading) =>
                      $debounce(() =>
                        searchProducts($event, loading, index, 'barcode')
                      )
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
                  >{{ $t("product_name") }}</label
                >
                <Field
                  required
                  rules="required"
                  type="text"
                  v-model="product.product_name"
                  :placeholder="$t('product_name')"
                  class="hidden"
                  :name="`${index}name`"
                  :id="`${index}name`"
                />
                <v-select
                  class="block w-full default-input !p-[1px]"
                  :class="errors[`${index}name`] ? 'ring-2 ring-red-500' : ''"
                  v-model="product.product_name"
                  @search="
                    ($event, loading) =>
                      $debounce(() =>
                        searchProducts($event, loading, index, 'name')
                      )
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
                  :placeholder="$t('product_name')"
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
                  :reduce="(t) => t.settings_value"
                  :label="`settings_value`"
                  type="text"
                  :placeholder="$t('measure')"
                >
                  <template v-slot:option="option">
                    {{ $t(option.settings_value) }}
                  </template>
                  <template v-slot:selected-option="option">
                    {{ $t(option.settings_value) }}
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
                  >{{ $t("expiration_date") }}
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
                  v-model="product.expiration_date"
                  :min="minDate"
                  type="date"
                  :class="
                    errors[`${index}product_expire`]
                      ? 'ring-2 ring-red-500'
                      : ''
                  "
                  class="default-input w-full"
                  :placeholder="$t('expiration_date')"
                  required
                />
                <span class="text-red-700">{{
                  errors[`${index}product_expire`]
                }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("purchased_price") }} ({{ $t("withoutTax") }})
                </label>
                <Field
                  required
                  rules="required"
                  type="number"
                  step="0.01"
                  v-model="product.purchased_price_wo_tax"
                  :placeholder="`${$t('purchased_price')} (${$t(
                    'withoutTax'
                  )})`"
                  class="default-input w-full"
                  :class="
                    errors[`${index}purchased_price`]
                      ? 'ring-2 ring-red-500'
                      : ''
                  "
                  :name="`${index}purchased_price_wo_tax`"
                  :id="`${index}purchased_price_wo_tax`"
                  @change="updatePurchasedPriceWTax(index)"
                />
                <span class="text-red-700">{{
                  errors[`${index}purchased_price`]
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
                  @change="updatePurchasedPriceWTax(index)"
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
                  :reduce="(t) => t.settings_value"
                  :label="`settings_value`"
                  type="text"
                  :placeholder="$t('tax')"
                  @option:selected="updatePurchasedPriceWTax(index)"
                >
                  <template v-slot:option="option">
                    {{ option.settings_value }}%
                  </template>
                  <template v-slot:selected-option="option">
                    {{ option.settings_value }}%
                  </template>
                </v-select>
                <span class="text-red-700">{{ errors[`${index}tax`] }}</span>
              </div>
              <div>
                <label
                  class="flex items-center gap-1 mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("purchased_price") }} ({{ $t("withTax") }})
                  <button
                    :id="`purchased-price-${index}-tooltip-btn`"
                    class="cursor-default"
                    type="button"
                    @mouseover="
                      $showTooltip({
                        targetEl: `purchased-price-${index}-tooltip`,
                        triggerEl: `purchased-price-${index}-tooltip-btn`,
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
                    :id="`purchased-price-${index}-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 dark:bg-neutral-900 rounded shadow-sm opacity-0 tooltip max-w-[250px]"
                  >
                    {{ $t("purchasedPriceWTaxCalculation") }}
                  </div>
                </label>
                <Field
                  type="number"
                  step="0.01"
                  v-model="product.purchased_price_w_tax"
                  :placeholder="`${$t('purchased_price')} (${$t('withTax')})`"
                  class="default-input !bg-neutral-100 cursor-not-allowed w-full"
                  :name="`${index}purchased_price_w_tax`"
                  :id="`${index}purchased_price_w_tax`"
                  :disabled="true"
                />
              </div>
              <div>
                <label
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >{{ $t("selling_price") }}</label
                >
                <Field
                  required
                  rules="required"
                  type="number"
                  step="0.01"
                  v-model="product.selling_price"
                  :placeholder="$t('selling_price')"
                  class="default-input w-full"
                  :class="
                    errors[`${index}selling_price`] ? 'ring-2 ring-red-500' : ''
                  "
                  :name="`${index}selling_price`"
                  :id="`${index}selling_price`"
                />
                <span class="text-red-700">{{
                  errors[`${index}selling_price`]
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
import ScannerDetector from "js-scanner-detection";
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
      purchase_types: [],
      isQrCode: false,
      activeIdx: 0,
      seller: {
        seller_name: "",
        invoice_number: "",
        fiscal_number: "",
        tax_number: "",
        purchase_date: new Date(),
        purchase_type: "purchase",
        search: "",
      },
      products: [
        {
          barcode: null,
          product_name: "",
          stock: null,
          tax: "18",
          rabat: "0",
          purchased_price_wo_tax: null,
          purchased_price_w_tax: null,
          selling_price: null,
          measure: "pcs",
          expiration_date: "",
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
      return this.$store.state.settingsModule.settings_type.tax;
    },
  },
  async created() {
    let options = {
      minLength: 4,
      endChar: [9, 13],
      onComplete: this.onComplete,
    };
    this.scannerDetector = new ScannerDetector(options);
    this.seller.purchase_date = this.minDate;
    await this.$store
      .dispatch("settingsModule/getSettingsType", {
        settings_type: "measure",
      })
      .then((response) => {
        this.measures = response.data;
      });
    await this.$store
      .dispatch("settingsModule/getSettingsType", {
        settings_type: "purchasetype",
      })
      .then((response) => {
        this.purchase_types = response.data;
      });
    await this.getSellers("");
    await this.getProducts("");
  },
  methods: {
    async onComplete(barcode) {
      this.isQrCode = true;
      await this.$store
        .dispatch("productModule/getProductDetailsByBarcode", barcode)
        .then((res) => {
          this.isQrCode = false;
          this.updateProductDetails(res.data, this.activeIdx);
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
    addProduct() {
      const product = {
        barcode: null,
        product_name: "",
        stock: null,
        tax: "18",
        rabat: "0",
        purchased_price_wo_tax: null,
        purchased_price_w_tax: null,
        selling_price: null,
        measure: "pcs",
        expiration_date: "",
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
      const seller_name = e.seller_name ? e.seller_name : e;
      this.seller.seller_name = seller_name;
      this.seller.search = null;
      const sellerInfo = this.sellers.find(
        (x) => x.seller_name.toLowerCase() === seller_name.toLowerCase()
      );
      if (sellerInfo) {
        this.seller.seller_name = sellerInfo?.seller_name;
        this.seller.fiscal_number = sellerInfo?.seller_fiscal_number;
        this.seller.tax_number = sellerInfo?.seller_tax_number;
      }
    },
    async searchProducts(search, loading, idx, type = "barcode") {
      if (this.isQrCode) return;
      this.products[idx].search = search;
      this.activeIdx = idx;
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
      const product_name = e.name ? e.name : e;
      this.products[idx].product_name = product_name;
      this.products[idx].search = null;
      const productInfo = this.productsList.find(
        (x) => x.name?.toLowerCase() === product_name.toLowerCase()
      );
      if (productInfo) {
        this.products[idx].product_name = productInfo.name;
        this.products[idx].barcode = productInfo.barcode;
        this.products[idx].tax = productInfo.tax;
        this.products[idx].selling_price = productInfo.selling_price;
        this.products[idx].purchased_price_wo_tax =
          productInfo.purchased_price_wo_tax;
        this.products[idx].expiration_date = productInfo.expiration_date;
        this.products[idx].measure = productInfo.measure;
        this.updatePurchasedPriceWTax(idx);
      }
    },
    getProductDetailsBarcode(e, idx) {
      if (this.isQrCode) return;
      const barcode = e.barcode ? Number(e.barcode) : Number(e);
      this.products[idx].barcode = barcode;
      this.products[idx].search = null;
      const productInfo = this.productsList.find((x) => x.barcode === barcode);
      if (productInfo) {
        this.products[idx].barcode = productInfo.barcode;
        this.updateProductDetails(productInfo, idx);
        this.updatePurchasedPriceWTax(idx);
      }
    },
    updateProductDetails(productInfo, idx) {
      this.products[idx].product_name = productInfo.name;
      this.products[idx].tax = productInfo.tax;
      this.products[idx].selling_price = productInfo.selling_price;
      this.products[idx].purchased_price_wo_tax =
        productInfo.purchased_price_wo_tax;
      this.products[idx].expiration_date = productInfo.expiration_date;
      this.products[idx].measure = productInfo.measure;
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
    saveBarcode(barcode, idx) {
      this.products[idx].barcode = barcode;
    },
    updatePurchasedPriceWTax(idx) {
      const { purchased_price_wo_tax, tax, rabat } = this.products[idx];

      const tax_percentage = Number(tax) / 100;
      const rabat_percentage = Number(rabat) / 100;
      const price_wo_rabat =
        purchased_price_wo_tax - purchased_price_wo_tax * rabat_percentage;
      const tax_amount = Number(price_wo_rabat * tax_percentage);
      const purchased_price_w_tax = Number(price_wo_rabat + tax_amount);

      this.products[idx].purchased_price_w_tax =
        purchased_price_w_tax.toFixed(4);
    },
  },
};
</script>
