<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <div class="full-layout">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center search-input-width">
          <label for="simple-search" class="sr-only">{{ $t("search") }}</label>
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
        <div class="flex flex-row items-center gap-2">
          <button
            @click="
              $router.push({
                name: 'new-purchase',
              })
            "
            v-if="$can('write', 'purchases')"
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
      <DateFilter
        :startDate="startDate"
        :endDate="endDate"
        :searchQuery="searchQuery"
        :dispatchModule="`purchaseModule/getPurchases`"
        @isTableLoading="isTableLoading = $event"
        @startDateChange="startDate = $event"
        @endDateChange="endDate = $event"
        @changeMonthDates="monthDates = $event"
      />
      <div class="overflow-hidden rounded-xl mb-5 min-h-65 relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style">
          <table
            class="w-full text-sm text-left text-gray-700 dark:text-gray-400"
          >
            <OverlayC v-if="isTableLoading" />
            <EmptyResultsC
              v-if="purchases.length === 0 && !isTableLoading"
              pluralText="Purchases"
              singularText="Purchase"
              routeName="new-purchase"
              :search="searchQuery"
            />
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
            >
              <tr>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('date_created')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("date") }}
                    <template v-if="sortColumn === 'date_created'">
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
                  <td class="py-2 px-6">
                    {{ purchase.dateCreated.substring(0, 10) }}
                  </td>
                  <td class="py-2 px-6">{{ purchase.id }}</td>
                  <td class="py-2 px-6">{{ purchase.sellerName }}</td>
                  <td class="py-2 px-6 max-w-xs">
                    {{ purchase.sellerInvoiceNumber }}
                  </td>
                  <td class="py-2 px-6">{{ purchase.subTotalAmount }} €</td>
                  <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
                  <td class="py-2 px-6">
                    <button
                      @click="
                        $router.push({
                          name: 'purchase-view',
                          params: { purchaseId: purchase.id },
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
          <th scope="col">
            {{ $t("date") }}
          </th>
          <th scope="col">ID</th>
          <th scope="col">
            {{ $t("sellerName") }}
          </th>
          <th scope="col">
            {{ $t("invoiceNumber") }}
          </th>
          <th scope="col">
            {{ $t("subtotalAmount") }}
          </th>
          <th scope="col">
            {{ $t("totalAmount") }}
          </th>
        </tr>
      </thead>
      <tbody>
        <template v-for="purchase in allPurchases" :key="purchase.id">
          <tr>
            <td>
              {{ purchase.dateCreated.substring(0, 10) }}
            </td>
            <td>{{ purchase.id }}</td>
            <td>{{ purchase.sellerName }}</td>
            <td>
              {{ purchase.sellerInvoiceNumber }}
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
import DateFilter from "@/components/DateFilterComponent.vue";
import HtmlToExcel from "@/services/mixins/HtmlToExcel";
export default {
  data() {
    return {
      isTableLoading: false,
      currentPage: 1,
      searchQuery: "",
      monthDates: [],
      startDate: "",
      endDate: "",
      sortColumn: null,
      sortDir: "desc",
      allPurchases: [],
    };
  },
  components: {
    DateFilter,
  },
  mixins: [HtmlToExcel],
  watch: {
    searchQuery: {
      async handler() {
        this.currentPage = 1;
        this.getPurchases(1);
      },
    },
  },
  async created() {
    const currentMonth = this.getMonth(new Date().getMonth() + 1);
    this.startDate = currentMonth.startDate;
    this.endDate = currentMonth.endDate;
    await this.getPurchases(this.currentPage);
    this.getAllPurchases();
  },
  computed: {
    purchases() {
      return this.$store.getters["purchaseModule/getPurchasesList"];
    },
    pagination() {
      return this.$store.getters["purchaseModule/getPurchasesPagination"];
    },
  },
  methods: {
    getMonth(v) {
      const month = String(v).padStart(2, "0");
      const year = new Date().getFullYear();
      const days = String(new Date(year, month, 0).getDate()).padStart(2, "0");

      return {
        startDate: `${year}-${month}-01`,
        endDate: `${year}-${month}-${days}`,
      };
    },
    async getPurchases(page) {
      this.isTableLoading = true;
      await this.$store
        .dispatch("purchaseModule/getPurchases", {
          page: page,
          startDate: this.startDate,
          endDate: this.endDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then((response) => {
          this.$store.commit("purchaseModule/SET_PURCHASES", response.data);
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
        .dispatch("purchaseModule/getPurchases", {
          page: 1,
          per_page: this.pagination.total,
          startDate: this.startDate,
          endDate: this.endDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
        })
        .then((response) => {
          this.allPurchases = response.data.data;
        });
    },
    async downloadExcel() {
      let fileName;
      const idx = this.$checkIfMonth(this.startDate, this.endDate);
      if (idx !== -1) {
        fileName = `${this.$t(
          this.$getMonths[idx + 1].value
        )}-${this.startDate.substring(0, 4)}-${this.$t("purchases")}`;
      } else {
        fileName = `${this.startDate}-TO-${this.endDate}`;
      }
      this.tableToExcel("table-data", fileName);
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getPurchases(this.currentPage);
      this.getAllPurchases();
    },
  },
};
</script>
