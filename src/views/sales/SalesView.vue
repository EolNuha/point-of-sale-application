<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <div class="full-layout flex flex-col">
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
              class="default-input w-full px-10"
              :placeholder="$t('search')"
            />
            <div
              v-if="showFilters"
              class="flex absolute inset-y-0 right-10 items-center pr-3 pointer-cursor"
            >
              <v-select
                class="min-w-[8rem] w-fit default-input"
                v-model="typeFilters"
                :placeholder="$t('type')"
                :options="[
                  { name: $t('regular'), value: true },
                  { name: $t('irregular'), value: false },
                ]"
                :reduce="(options) => options.value"
                :clearable="false"
                :multiple="true"
                label="name"
              ></v-select>
            </div>
            <button
              class="flex absolute inset-y-0 right-0 items-center pointer-cursor p-2.5 rounded-full hover:bg-gray-300/50 dark:hover:bg-neutral-600"
              @click="showFilters = !showFilters"
            >
              <IconC
                v-if="!showFilters"
                iconName="FunnelIcon"
                iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
              />
              <IconC
                v-else
                iconName="XMarkIcon"
                iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
              />
            </button>
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
            class="theme-gradient-btn inline-flex items-center text-center"
          >
            <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
            {{ $t("newSale") }}
          </button>
          <button
            @click="downloadExcel()"
            class="green-gradient-btn inline-flex items-center text-center"
            :disabled="!(sales?.length > 0)"
          >
            <div
              class="inline-flex flex-row"
              role="status"
              v-if="isExcelLoading"
            >
              <IconC
                iconType="custom"
                iconName="SpinnerIcon"
                iconClass="mr-2 w-5 h-5 text-gray-200 animate-spin fill-white"
              />
              {{ $t("downloading") }}...
              <span class="sr-only">Loading...</span>
            </div>
            <div class="inline-flex flex-row" v-else>
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
        :dispatchModule="`saleModule/getSales`"
        @isTableLoading="isTableLoading = $event"
        @startDateChange="startDate = $event"
        @endDateChange="endDate = $event"
        @changeMonthDates="monthDates = $event"
      />
      <div class="overflow-hidden rounded mb-5 flex grow relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style grow">
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="sales?.length === 0 && !isTableLoading"
            pluralText="Sales"
            singularText="Sale"
            :search="searchQuery"
            routeName="new-sale"
          />
          <table
            class="bg-white dark:bg-neutral-800 w-full text-sm text-left text-gray-700 dark:text-gray-400"
          >
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
                  class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:bg-gray-100/75 dark:hover:bg-neutral-900/[.5]"
                >
                  <td class="py-2 px-6">
                    {{ sale.dateCreated?.substring(0, 10) }}
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
                          query: {
                            saleDate: sale.dateCreated?.substring(0, 10),
                          },
                        })
                      "
                      class="p-2.5 rounded-full hover:bg-gray-300/50 dark:hover:bg-neutral-700"
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
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getSales($event)"
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
      isExcelLoading: false,
      currentPage: 1,
      searchQuery: "",
      startDate: "",
      endDate: "",
      sortColumn: null,
      sortDir: "desc",
      allSales: [],
      showFilters: false,
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
        this.getSales(1);
      },
    },
    typeFilters: {
      async handler() {
        this.currentPage = 1;
        this.getSales(1);
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
    typeFilters: {
      get() {
        return this.$store.state.saleModule.typeFilters;
      },
      set(v) {
        this.$store.state.saleModule.typeFilters = v;
      },
    },
  },
  async created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    const currentMonth = this.getMonth(new Date().getMonth() + 1);
    this.currentMonth = new Date().getMonth() + 1;
    this.startDate = currentMonth.startDate;
    this.endDate = currentMonth.endDate;
    await this.getSales(this.currentPage);
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
    async getSales(page) {
      this.isTableLoading = true;
      await this.$store
        .dispatch("saleModule/getSales", {
          page: page,
          startDate: this.startDate,
          endDate: this.endDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
          type_filter: this.typeFilters,
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
    async getAllSales() {
      await this.$store
        .dispatch("saleModule/getAllSales", {
          page: 1,
          per_page: this.pagination.total,
          startDate: this.startDate,
          endDate: this.endDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
          type_filter: this.typeFilters,
        })
        .then((response) => {
          this.allSales = response.data.data;
        });
    },
    async downloadExcel() {
      this.isExcelLoading = true;
      await this.getAllSales();
      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let dateTh = document.createElement("th");
      dateTh.innerHTML = this.$t("date");
      headTr.appendChild(dateTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("td");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }

      let subtotalTh = document.createElement("th");
      subtotalTh.innerHTML = this.$t("subtotalAmount");
      headTr.appendChild(subtotalTh);

      let totalTh = document.createElement("th");
      totalTh.innerHTML = this.$t("totalAmount");
      headTr.appendChild(totalTh);

      for await (const element of this.allSales) {
        let bodyTr = document.createElement("tr");
        let dateTd = document.createElement("td");
        dateTd.innerHTML = element.dateCreated?.substring(0, 10);
        bodyTr.appendChild(dateTd);
        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${this.getTaxValue(
            element.taxes,
            tax.settingsAlias
          )} €`;
          bodyTr.appendChild(taxTd);
        }
        let subtotalTd = document.createElement("td");
        subtotalTd.innerHTML = `${element.subTotalAmount} €`;
        let totalTd = document.createElement("td");
        totalTd.innerHTML = `${element.totalAmount} €`;
        bodyTr.appendChild(subtotalTd);
        bodyTr.appendChild(totalTd);
        tbody.appendChild(bodyTr);
      }

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);

      let fileName;
      const idx = this.$checkIfMonth(this.startDate, this.endDate);
      if (idx !== -1) {
        fileName = `${this.$t(
          this.$getMonths[idx + 1].value
        )}-${this.startDate?.substring(0, 4)}-${this.$t("sales")}`;
      } else {
        fileName = `${this.startDate}-TO-${this.endDate}`;
      }
      this.tableToExcel(table, fileName);
      this.isExcelLoading = false;
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getSales(this.currentPage);
    },
  },
};
</script>
