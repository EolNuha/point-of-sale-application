<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <div class="full-layout">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <div class="flex items-center search-input-width">
            <label for="simple-search" class="sr-only">{{
              $t("search")
            }}</label>
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
                @input="
                  $debounce(() => {
                    searchQuery = $event.target.value;
                  })
                "
                type="text"
                class="default-input w-full pl-10"
                :placeholder="$t('search')"
              />
            </div>
          </div>
        </div>
        <div class="flex flex-row items-center gap-2">
          <button
            @click="
              $router.push({
                name: 'new-purchase',
              })
            "
            class="theme-gradient-btn inline-flex items-center text-center"
          >
            <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
            {{ $t("newPurchase") }}
          </button>
          <button
            @click="downloadExcel()"
            class="green-gradient-btn inline-flex items-center text-center"
            :disabled="!(allPurchases?.length > 0)"
          >
            <div class="inline-flex flex-row">
              <IconC
                iconType="custom"
                iconName="ExcelFileIcon"
                iconClass="w-5 h-5 fill-white mr-2"
              />
              {{ $t("download") }} Excel
            </div>
          </button>
        </div>
      </div>
      <h2 class="text-gray-700 dark:text-gray-300 text-2xl font-extrabold my-3">
        {{ $t("date") }}: {{ purchaseDate?.substring(0, 10) }}
      </h2>
      <div class="overflow-hidden rounded-xl mb-5 min-h-65 relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style">
          <table
            class="w-full text-sm text-left text-gray-700 dark:text-gray-400"
          >
            <OverlayC v-if="isTableLoading" />
            <EmptyResultsC
              v-if="purchases?.length === 0 && !isTableLoading"
              pluralText="Purchases"
              singularText="Purchase"
              :search="searchQuery"
              routeName="new-purchase"
            />
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
            >
              <tr>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('id')"
                >
                  <div class="flex justify-between items-center">
                    ID
                    <template v-if="sortColumn === 'id'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('seller_name')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("sellerName") }}
                    <template v-if="sortColumn === 'seller_name'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('seller_invoice_number')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("invoiceNumber") }}
                    <template v-if="sortColumn === 'seller_invoice_number'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
                  v-for="item in taxes"
                  :key="item.settingsValue"
                >
                  {{ item.settingsName }}%
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('subtotal_amount')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("subtotalAmount") }}
                    <template v-if="sortColumn === 'subtotal_amount'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('total_amount')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("totalAmount") }}
                    <template v-if="sortColumn === 'total_amount'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th scope="col" class="py-3 px-6"></th>
              </tr>
            </thead>
            <tbody>
              <template v-for="purchase in purchases" :key="purchase.id">
                <tr
                  class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:dark:bg-neutral-900/75"
                >
                  <td class="py-2 px-6">{{ purchase.id }}</td>
                  <td class="py-2 px-6">{{ purchase.sellerName }}</td>
                  <td class="py-2 px-6">{{ purchase.sellerInvoiceNumber }}</td>
                  <td
                    class="py-2 px-6"
                    v-for="item in taxes"
                    :key="item.settingsValue"
                  >
                    {{ getTaxValue(purchase.taxes, item.settingsAlias) }} €
                  </td>
                  <td class="py-2 px-6">{{ purchase.subTotalAmount }} €</td>
                  <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
                  <td class="py-2 px-6">
                    <button
                      @click="
                        $router.push({
                          name: 'purchase-view',
                          params: { purchaseId: purchase.id },
                          query: { purchaseDate: purchaseDate },
                        })
                      "
                      class="p-2.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-neutral-800/50"
                    >
                      <IconC
                        iconName="DocumentMagnifyingGlassIcon"
                        iconClass="h-5 w-5 text-gray-900 dark:text-gray-300"
                      />
                    </button>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <table id="table-data" class="hidden">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">{{ $t("sellerName") }}</th>
          <th scope="col">{{ $t("invoiceNumber") }}</th>
          <th scope="col" v-for="item in taxes" :key="item.settingsValue">
            {{ $t("tax") }} {{ item.settingsName }}%
          </th>
          <th scope="col">{{ $t("subtotalAmount") }}</th>
          <th scope="col">{{ $t("totalAmount") }}</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="purchase in allPurchases" :key="purchase.id">
          <tr>
            <td>
              {{ purchase.id }}
            </td>
            <td>{{ purchase.sellerName }}</td>
            <td>{{ purchase.sellerInvoiceNumber }}</td>
            <td v-for="item in taxes" :key="item.settingsValue">
              {{ getTaxValue(purchase.taxes, item.settingsAlias) }} €
            </td>
            <td>{{ purchase.subTotalAmount }} €</td>
            <td>{{ purchase.totalAmount }} €</td>
          </tr>
        </template>
      </tbody>
    </table>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getPurchases($event)"
    />
  </div>
</template>

<script>
import HtmlToExcel from "@/services/mixins/HtmlToExcel";
export default {
  data() {
    return {
      isTableLoading: false,
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      allPurchases: [],
    };
  },
  mixins: [HtmlToExcel],
  computed: {
    purchases() {
      return this.$store.getters["purchaseModule/getPurchasesList"];
    },
    pagination() {
      return this.$store.getters["purchaseModule/getPurchasesPagination"];
    },
    purchaseDate() {
      return this.$route.query.purchaseDate;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
  },
  watch: {
    searchQuery: {
      async handler() {
        this.currentPage = 1;
        this.getPurchases(1);
      },
    },
    "$store.state.purchaseModule.purchases": {
      handler() {
        this.getAllPurchases();
      },
    },
  },
  async created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.getPurchases(this.currentPage);
  },
  methods: {
    getTaxValue(arr, alias) {
      return (
        arr.find((x) => x.taxAlias === alias)?.taxValue || Number(0).toFixed(2)
      );
    },
    async getPurchases(page) {
      this.isTableLoading = true;
      await this.$store
        .dispatch("purchaseModule/getDailyPurchases", {
          page: page,
          date: this.purchaseDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    async getAllPurchases() {
      await this.$store
        .dispatch("purchaseModule/getAllDailyPurchases", {
          page: 1,
          per_page: 1000,
          date: this.purchaseDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then((response) => {
          this.allPurchases = response.data.data;
        });
    },
    async downloadExcel() {
      let fileName =
        this.purchaseDate.replaceAll(".", "-") + `-${this.$t("purchases")}`;
      this.tableToExcel("table-data", fileName);
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getPurchases(this.currentPage);
    },
  },
};
</script>
