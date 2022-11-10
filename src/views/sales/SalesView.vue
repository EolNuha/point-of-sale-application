<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
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
              name: 'new-sale',
            })
          "
          v-if="$can('write', 'sales')"
          class="blue-gradient-btn inline-flex items-center text-center"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
          {{ $t("newSale") }}
        </button>
        <button
          @click="downloadExcel()"
          class="green-gradient-btn inline-flex items-center text-center"
        >
          <div class="inline-flex flex-row" role="status" v-if="isExcelLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-5 h-5 text-gray-200 animate-spin fill-white"
            />
            Downloading...
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else class="inline-flex flex-row">
            <IconC
              iconType="custom"
              iconName="ExcelFileIcon"
              iconClass="w-5 h-5 fill-white mr-2"
            />
            Download Excel
          </div>
        </button>
      </div>
    </div>
    <DateFilter
      :startDate="startDate"
      :endDate="endDate"
      :searchQuery="searchQuery"
      :dispatchModule="`saleModule/getSales`"
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
            v-if="sales.length === 0 && !isTableLoading"
            pluralText="Sales"
            singularText="Sale"
            :search="searchQuery"
            routeName="new-sale"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
                v-for="item in taxes"
                :key="item.settingsValue"
              >
                {{ $t("tax") }} {{ item.settingsName }}%
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
            <template v-for="sale in sales" :key="sale.id">
              <tr
                class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:dark:bg-neutral-900/75"
              >
                <td class="py-2 px-6">
                  {{ sale.dateCreated.substring(0, 10) }}
                </td>
                <td
                  class="py-2 px-6"
                  v-for="item in taxes"
                  :key="item.settingsValue"
                >
                  {{ getTaxValue(sale.taxes, item.settingsAlias) }} €
                </td>
                <td class="py-2 px-6">{{ sale.subTotalAmount }} €</td>
                <td class="py-2 px-6">{{ sale.totalAmount }} €</td>
                <td class="py-2 px-6">
                  <button
                    @click="
                      $router.push({
                        name: 'daily-sales',
                        query: { saleDate: sale.dateCreated.substring(0, 10) },
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
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getSales($event)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isTableLoading: false,
      isExcelLoading: false,
      currentPage: 1,
      searchQuery: "",
      startDate: "",
      endDate: "",
      sortColumn: null,
      sortDir: "desc",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.currentPage = 1;
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("saleModule/getSales", {
            page: this.currentPage,
            search: value,
            startDate: this.startDate,
            endDate: this.endDate,
            sort_column: this.sortColumn,
            sort_dir: this.sortDir,
          });
          this.isTableLoading = false;
        } catch {
          this.isTableLoading = false;
        }
      },
    },
  },
  computed: {
    sales() {
      return this.$store.getters["saleModule/getSalesList"];
    },
    pagination() {
      return this.$store.getters["saleModule/getSalesPagination"];
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
  },
  created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    const currentMonth = this.getMonth(new Date().getMonth() + 1);
    this.currentMonth = new Date().getMonth() + 1;
    this.startDate = currentMonth.startDate;
    this.endDate = currentMonth.endDate;
    this.getSales(this.currentPage);
  },
  methods: {
    getTaxValue(arr, alias) {
      return (
        arr.find((x) => x.taxAlias === alias)?.taxValue || Number(0).toFixed(2)
      );
    },
    getMonth(v) {
      const month = String(v).padStart(2, "0");
      const year = new Date().getFullYear();
      const days = String(new Date(year, month, 0).getDate()).padStart(2, "0");

      return {
        startDate: `${year}-${month}-01`,
        endDate: `${year}-${month}-${days}`,
      };
    },
    getSales(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("saleModule/getSales", {
          page: page,
          startDate: this.startDate,
          endDate: this.endDate,
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
    async downloadExcel() {
      this.isExcelLoading = true;
      let fileName;
      const idx = this.$checkIfMonth(this.startDate, this.endDate);
      if (idx !== -1) {
        fileName = `${this.$t(
          this.$getMonths[idx + 1].value
        )}-${this.startDate.substring(0, 4)}-${this.$t("sales")}`;
      } else {
        fileName = `${this.startDate}-TO-${this.endDate}`;
      }
      const data = {
        fileName: fileName,
        page: 1,
        per_page: this.pagination.total,
        startDate: this.startDate,
        endDate: this.endDate,
      };
      this.$store
        .dispatch("saleModule/downloadExcelFile", data)
        .then(() => {
          this.isExcelLoading = false;
          this.$toast.success(this.$t("excelFileDownloaded"));
        })
        .catch(() => {
          this.isExcelLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getSales(this.currentPage);
    },
  },
};
</script>
