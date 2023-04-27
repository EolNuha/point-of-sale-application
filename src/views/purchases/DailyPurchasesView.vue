<!-- eslint-disable no-undef -->
<template>
  <div class="main-div">
    <div class="full-layout flex flex-col">
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
                  :options="purchaseTypes"
                  :reduce="(t) => t.settingsValue"
                  :label="`settingsValue`"
                  :clearable="false"
                  :multiple="true"
                >
                  <template v-slot:option="option">
                    {{ $t(option.settingsValue) }}
                  </template>
                  <template v-slot:selected-option="option">
                    {{ $t(option.settingsValue) }}
                  </template></v-select
                >
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
            :disabled="!(purchases?.length > 0)"
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
      <h2 class="text-gray-700 dark:text-gray-300 text-2xl font-extrabold my-3">
        {{ $t("date") }}: {{ purchaseDate?.substring(0, 10) }}
      </h2>
      <div class="overflow-hidden rounded mb-5 flex grow relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style grow">
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="purchases?.length === 0 && !isTableLoading"
            pluralText="Purchases"
            singularText="Purchase"
            :search="searchQuery"
            routeName="new-purchase"
          />
          <detailed-view
            :purchases="purchases"
            :taxes="taxes"
            @sort="sort($event)"
            @reload="getPurchases(currentPage)"
          />
        </div>
      </div>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getPurchases($event)"
    />
  </div>
</template>

<script>
import { utils, writeFileXLSX } from "xlsx";
import PurchaseTables from "@/services/mixins/PurchaseTables";
import DetailedView from "./DetailedView.vue";
export default {
  data() {
    return {
      isTableLoading: true,
      isExcelLoading: false,
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      allPurchases: [],
      selectedPurchase: [],
      showFilters: false,
      typeFilters: [],
      purchaseTypes: [],
    };
  },
  components: {
    DetailedView,
  },
  mixins: [PurchaseTables],
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
    typeFilters: {
      async handler() {
        this.currentPage = 1;
        this.getPurchases(1);
      },
    },
  },
  async created() {
    await this.$store
      .dispatch("settingsModule/getSettingsType", {
        settingsType: "purchasetype",
      })
      .then((response) => {
        this.purchaseTypes = response.data;
      });
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.getPurchases(this.currentPage);
  },
  methods: {
    async getPurchases(page) {
      this.isTableLoading = true;
      await this.$store
        .dispatch("purchaseModule/getDailyPurchases", {
          page: page,
          date: this.purchaseDate,
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
    async getAllPurchases() {
      await this.$store
        .dispatch("purchaseModule/getAllDailyPurchases", {
          page: 1,
          per_page: this.pagination.total,
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
      this.isExcelLoading = true;
      await this.getAllPurchases();

      let table = await this.gridExcelView();
      let fileName =
        this.purchaseDate.replaceAll(".", "-") + `-${this.$t("purchases")}`;

      const wb = utils.table_to_book(table);
      await writeFileXLSX(wb, `${fileName}.xlsx`);
      this.isExcelLoading = false;
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getPurchases(this.currentPage);
    },
    deletePurchase(purchase) {
      this.selectedPurchase = purchase;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
  },
};
</script>
