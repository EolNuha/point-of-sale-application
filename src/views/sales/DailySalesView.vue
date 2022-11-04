<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2">
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
      </div>
      <div class="flex flex-row items-center gap-2">
        <button
          @click="
            $router.push({
              name: 'new-sale',
            })
          "
          class="blue-gradient-btn inline-flex items-center text-center"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
          New Sale
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
    <h2 class="text-gray-700 dark:text-gray-300 text-2xl font-extrabold my-3">
      {{ $t("date") }}: {{ saleDate.substring(0, 10) }}
    </h2>
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
            class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400 cursor-default"
          >
            <tr>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600 cursor-not-allowed"
                v-for="item in taxes"
                :key="item.settingsValue"
              >
                {{ item.settingsName }}%
              </th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('user')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("user") }}
                  <template v-if="sortColumn === 'user'">
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
                class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
              >
                <td class="py-2 px-6">{{ sale.id }}</td>
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
                  {{ sale.user.firstName }} {{ sale.user.lastName }}
                </td>
                <td class="py-2 px-6">
                  <button
                    @click="
                      $router.push({
                        name: 'sale-view',
                        params: { saleId: sale.id },
                        query: { saleDate: saleDate },
                      })
                    "
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
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
      sortColumn: null,
      sortDir: "desc",
    };
  },
  computed: {
    sales() {
      return this.$store.getters["saleModule/getSalesList"];
    },
    pagination() {
      return this.$store.getters["saleModule/getSalesPagination"];
    },
    saleDate() {
      return this.$route.query.saleDate;
    },
    taxes() {
      return this.$store.state.settingsModule.settingsType;
    },
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.currentPage = 1;
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("saleModule/getDailySales", {
            page: this.currentPage,
            search: value,
            date: this.saleDate,
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
  created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    this.getSales(this.currentPage);
  },
  methods: {
    getTaxValue(arr, alias) {
      return (
        arr.find((x) => x.taxAlias === alias)?.taxValue || Number(0).toFixed(2)
      );
    },
    getSales(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("saleModule/getDailySales", {
          page: page,
          date: this.saleDate,
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
      const data = {
        fileName: this.saleDate.replaceAll(".", "-") + `-${this.$t("sales")}`,
        dailySales: true,
        dailyDate: this.saleDate,
        page: 1,
        per_page: this.pagination.total,
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
