<!-- eslint-disable no-undef -->
<template>
  <div class="main-div">
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
              @input="searchQuery = $event.target.value"
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
              class="flex absolute inset-y-0 right-0 items-center pointer-cursor p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-600"
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
      <div class="flex items-center justify-between w-full">
        <DateFilter
          :startDate="startDate"
          :endDate="endDate"
          :searchQuery="searchQuery"
          :dispatchModule="salesDispatch"
          @isTableLoading="isTableLoading = $event"
          @startDateChange="startDate = $event"
          @endDateChange="endDate = $event"
          @changeMonthDates="monthDates = $event"
        />
        <button
          type="button"
          @click="switchView"
          class="p-1.5 hover:bg-neutral-300 rounded dark:hover:bg-neutral-700 flex items-center gap-2 dark:text-gray-200"
        >
          <IconC
            iconType="custom"
            iconName="GridIcon"
            iconClass="w-6 h-6"
            v-if="!detailedView"
          />
          <IconC
            iconType="custom"
            iconName="TableIcon"
            iconClass="w-6 h-6"
            v-else
          />
          {{ detailedView ? $t("groupedView") : $t("detailedView") }}
        </button>
      </div>
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
          <detailed-view
            v-if="detailedView"
            :sales="sales"
            :taxes="taxes"
            :pagination="pagination"
            @sort="sort($event)"
            @reload="getSales(currentPage)"
          />
          <grouped-view
            v-else
            :sales="sales"
            :taxes="taxes"
            :pagination="pagination"
            @sort="sort($event)"
          />
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
import debounce from "lodash/debounce";
import DateFilter from "@/components/DateFilterComponent.vue";
import JsonToExcel from "@/services/mixins/JsonToExcel";
import DetailedView from "./DetailedView.vue";
import GroupedView from "./GroupedView.vue";

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
      detailedView: true,
      debouncedGetSales: null,
    };
  },
  components: {
    DateFilter,
    DetailedView,
    GroupedView,
  },
  mixins: [JsonToExcel],
  watch: {
    searchQuery: {
      async handler() {
        this.currentPage = 1;
        this.debouncedGetSales(1);
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
      return this.$store.state.settingsModule.settings_type.tax?.filter(
        (item) => item.settings_alias !== "zero"
      );
    },
    typeFilters: {
      get() {
        return this.$store.state.saleModule.typeFilters;
      },
      set(v) {
        this.$store.state.saleModule.typeFilters = v;
      },
    },
    salesDispatch() {
      return this.detailedView
        ? "saleModule/getSalesDetailed"
        : "saleModule/getSales";
    },
    allSalesDispatch() {
      return this.detailedView
        ? "saleModule/getSalesDetailedExcel"
        : "saleModule/getSalesGroupedExcel";
    },
    fileName() {
      let fileName;
      const idx = this.$checkIfMonth(this.startDate, this.endDate);
      if (idx !== -1) {
        fileName = `${this.$t(
          this.$getMonths[idx + 1].value
        )}-${this.startDate?.substring(0, 4)}-${this.$t("sales")}`;
      } else {
        fileName = `${this.startDate}-${this.$t("to")}-${this.endDate}`;
      }
      return fileName;
    },
  },
  async created() {
    this.debouncedGetSales = debounce(this.getSales, 500);
    const currentMonth = this.getMonth(new Date().getMonth() + 1);
    this.currentMonth = new Date().getMonth() + 1;
    this.startDate = currentMonth.startDate;
    this.endDate = currentMonth.endDate;
    await this.getSales(this.currentPage);
  },
  methods: {
    switchView() {
      this.detailedView = !this.detailedView;
      this.getSales(this.currentPage);
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
        .dispatch(this.salesDispatch, {
          page: page,
          start_date: this.startDate,
          end_date: this.endDate,
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
        .dispatch(this.allSalesDispatch, {
          start_date: this.startDate,
          end_date: this.endDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
          file_name: this.fileName,
        })
        .then((response) => {
          this.allSales = response.data;
          if (this.detailedView) {
            console.log(response.data);
            const fileURL = URL.createObjectURL(new Blob([response.data]));
            const fileLink = document.createElement("a");
            fileLink.href = fileURL;
            fileLink.setAttribute("download", `${this.fileName}.xlsx`);
            document.body.appendChild(fileLink);

            fileLink.click();

            document.body.removeChild(fileLink);
            window.URL.revokeObjectURL(fileURL);
            this.isExcelLoading = false;
          }
        });
    },
    async downloadExcel() {
      this.isExcelLoading = true;
      await this.getAllSales();
      if (this.detailedView) return;
      await this.jsonToExcel(this.allSales, this.fileName);
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
