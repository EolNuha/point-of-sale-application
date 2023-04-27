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
        </div>
        <div class="flex flex-row items-center gap-2">
          <button
            @click="
              $router.push({
                name: 'new-sale',
              })
            "
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
      <h2 class="text-gray-700 dark:text-gray-300 text-2xl font-extrabold my-3">
        {{ $t("date") }}: {{ saleDate?.substring(0, 10) }}
      </h2>
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
              class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
            >
              <tr>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('user')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("employee") }}
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
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('is_regular')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("type") }}
                    <template v-if="sortColumn === 'is_regular'">
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
                  v-for="item in taxes"
                  :key="item.settingsValue"
                >
                  {{ item.settingsName }}%
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('gross_profit_amount')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("grossProfit") }}
                    <template v-if="sortColumn === 'gross_profit_amount'">
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
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('net_profit_amount')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("netProfit") }}
                    <template v-if="sortColumn === 'net_profit_amount'">
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
                  class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:bg-neutral-100/75 dark:hover:bg-neutral-900/[.5]"
                >
                  <td class="py-2 px-6">{{ sale.id }}</td>
                  <td class="py-2 px-6">
                    {{ sale.user?.firstName }} {{ sale.user?.lastName }}
                  </td>
                  <td class="py-2 px-6">
                    {{ sale.isRegular ? $t("regular") : $t("irregular") }}
                  </td>
                  <td
                    class="py-2 px-6"
                    v-for="item in taxes"
                    :key="item.settingsValue"
                  >
                    {{
                      sale.taxes
                        ? sale.taxes[item.settingsAlias]?.taxValue || "0.00"
                        : "0.00"
                    }}
                    €
                  </td>
                  <td class="py-2 px-6">{{ sale.subTotalAmount }} €</td>
                  <td class="py-2 px-6">{{ sale.totalAmount }} €</td>
                  <td class="py-2 px-6">{{ sale.grossProfitAmount }} €</td>
                  <td class="py-2 px-6">{{ sale.netProfitAmount }} €</td>
                  <td class="py-2 px-6 w-1.5" v-if="$can('read', 'sales')">
                    <button
                      class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                      :id="`sale-${sale.id}-btn`"
                      @click="
                        $toggleDropdown({
                          targetEl: `sale-${sale.id}-menu`,
                          triggerEl: `sale-${sale.id}-btn`,
                          placementEl: 'left',
                        })
                      "
                    >
                      <IconC
                        iconName="EllipsisVerticalIcon"
                        iconClass="w-5 h-5 cursor-pointer"
                      />
                    </button>
                    <div
                      :id="`sale-${sale.id}-menu`"
                      class="hidden z-10 w-[8rem] bg-white rounded shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800"
                      style="inset: 0px auto auto -300px !important"
                    >
                      <ul
                        class="py-1 text-sm font-normal text-gray-700 cursor-pointer divide-y divide-gray-300 dark:divide-gray-700"
                        aria-labelledby="dropdownDefault"
                      >
                        <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'sale-view',
                              params: { saleId: sale.id },
                              query: { saleDate: saleDate },
                            })
                          "
                        >
                          <IconC
                            iconName="DocumentMagnifyingGlassIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("viewDocument") }}
                        </li>
                        <!-- <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'sale-edit',
                              params: { saleId: sale.id },
                              query: { saleDate: saleDate },
                            })
                          "
                          v-if="$can('execute', 'sales')"
                        >
                          <IconC
                            iconType="solid"
                            iconName="PencilIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("edit") }}
                        </li> -->
                        <li
                          class="inline-flex text-red-700 dark:text-red-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="deleteSale(sale)"
                          v-if="$can('execute', 'sales')"
                        >
                          <IconC
                            iconName="TrashIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("delete") }}
                        </li>
                      </ul>
                    </div>
                  </td>
                </tr>
              </template>
              <tr
                v-if="sales?.length !== 0"
                class="text-md uppercase font-bold bg-white border-b dark:bg-neutral-900 dark:border-gray-700"
              >
                <td class="py-4 px-6">{{ $t("total") }}</td>
                <td class="py-4 px-6">-</td>
                <td class="py-4 px-6">-</td>
                <td
                  class="py-2 px-6"
                  v-for="item in pagination.taxes"
                  :key="item.settingsValue"
                >
                  {{ item.taxValue }} €
                </td>
                <td class="py-4 px-6">
                  {{ pagination.salesSubTotalAmount }} €
                </td>
                <td class="py-4 px-6">{{ pagination.salesTotalAmount }} €</td>
                <td class="py-4 px-6">
                  {{ pagination.salesTotalGrossProfit }} €
                </td>
                <td class="py-4 px-6">
                  {{ pagination.salesTotalNetProfit }} €
                </td>
                <td class="py-4 px-6"></td>
              </tr>
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
    <delete-modal
      :itemId="selectedSale.id"
      deleteAction="saleModule/deleteSale"
      :title="$t('sale')"
      deleteRef="delete-modal"
      @reload="getSales(currentPage)"
    >
    </delete-modal>
  </div>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
import { utils, writeFileXLSX } from "xlsx";
export default {
  data() {
    return {
      isTableLoading: false,
      isExcelLoading: false,
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      allSales: [],
      selectedSale: [],
      showFilters: false,
    };
  },
  components: {
    DeleteModal,
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
    typeFilters: {
      get() {
        return this.$store.state.saleModule.typeFilters;
      },
      set(v) {
        this.$store.state.saleModule.typeFilters = v;
      },
    },
  },
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
  async created() {
    this.$store.dispatch("settingsModule/getSettingsType", {
      settingsType: "tax",
    });
    await this.getSales(this.currentPage);
  },
  methods: {
    async getSales(page) {
      this.isTableLoading = true;
      await this.$store
        .dispatch("saleModule/getDailySales", {
          page: page,
          date: this.saleDate,
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
        .dispatch("saleModule/getAllDailySales", {
          page: 1,
          per_page: this.pagination.total,
          date: this.saleDate,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
          type_filter: this.typeFilters,
        })
        .then((response) => {
          this.allSales = response.data;
        });
    },
    async downloadExcel() {
      this.isExcelLoading = true;
      await this.getAllSales();

      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let idTh = document.createElement("th");
      idTh.innerHTML = "ID";
      headTr.appendChild(idTh);

      let employeeTh = document.createElement("th");
      employeeTh.innerHTML = this.$t("employee");
      headTr.appendChild(employeeTh);

      let typeTh = document.createElement("th");
      typeTh.innerHTML = this.$t("type");
      headTr.appendChild(typeTh);

      for await (const tax of this.taxes) {
        let taxTh = document.createElement("th");
        taxTh.innerHTML = `${this.$t("tax")} ${tax.settingsName}%`;
        headTr.appendChild(taxTh);
      }
      for await (const item of [
        "subtotalAmount",
        "totalAmount",
        "grossProfit",
        "netProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = this.$t(item);
        headTr.appendChild(itemTh);
      }

      for await (const element of this.allSales.data) {
        let bodyTr = document.createElement("tr");

        let idTd = document.createElement("td");
        idTd.innerHTML = element.id;
        bodyTr.appendChild(idTd);
        let employeeTd = document.createElement("td");
        employeeTd.innerHTML = `${element.user.firstName} ${element.user.lastName}`;
        bodyTr.appendChild(employeeTd);
        let typeTd = document.createElement("td");
        typeTd.innerHTML = element.isRegular
          ? this.$t("regular")
          : this.$t("irregular");
        bodyTr.appendChild(typeTd);

        for await (const tax of this.taxes) {
          let taxTd = document.createElement("td");
          taxTd.innerHTML = `${
            element.taxes
              ? element.taxes[tax.settingsAlias]?.taxValue || "0.00"
              : "0.00"
          } €`;
          bodyTr.appendChild(taxTd);
        }

        for await (const item of [
          "subTotalAmount",
          "totalAmount",
          "grossProfitAmount",
          "netProfitAmount",
        ]) {
          let itemTd = document.createElement("td");
          itemTd.innerHTML = `${element[item]} €`;
          bodyTr.appendChild(itemTd);
        }
        tbody.appendChild(bodyTr);
      }

      let totalTr = document.createElement("tr");
      let bottomTd = document.createElement("th");
      bottomTd.innerHTML = this.$t("total");
      totalTr.appendChild(bottomTd);
      let emptyTd = document.createElement("th");
      emptyTd.innerHTML = "-";
      totalTr.appendChild(emptyTd);
      let empty1Td = document.createElement("th");
      empty1Td.innerHTML = "-";
      totalTr.appendChild(empty1Td);
      for await (const tax of this.allSales.pagination.taxes) {
        let taxTd = document.createElement("th");
        taxTd.innerHTML = `${tax.taxValue} €`;
        totalTr.appendChild(taxTd);
      }
      for await (const item of [
        "salesSubTotalAmount",
        "salesTotalAmount",
        "salesTotalGrossProfit",
        "salesTotalNetProfit",
      ]) {
        let itemTh = document.createElement("th");
        itemTh.innerHTML = `${this.allSales.pagination[item]} €`;
        totalTr.appendChild(itemTh);
      }

      tbody.appendChild(totalTr);

      thead.appendChild(headTr);
      table.appendChild(thead);
      table.appendChild(tbody);
      let fileName =
        this.saleDate.replaceAll(".", "-") + `-${this.$t("sales")}`;

      const wb = utils.table_to_book(table);
      await writeFileXLSX(wb, `${fileName}.xlsx`);
      this.isExcelLoading = false;
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getSales(this.currentPage);
    },
    deleteSale(sale) {
      this.selectedSale = sale;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
  },
};
</script>
