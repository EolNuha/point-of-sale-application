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
      <div class="overflow-hidden rounded-xl mb-5 min-h-65 relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style">
          <table
            class="bg-white dark:bg-neutral-800 w-full text-sm text-left text-gray-700 dark:text-gray-400"
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
                  class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:bg-gray-100/75 dark:hover:bg-neutral-900/[.5]"
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
                  <td class="py-2 px-6 w-1.5" v-if="$can('read', 'purchases')">
                    <button
                      class="p-2.5 rounded-full hover:bg-gray-300/50 dark:hover:bg-neutral-700"
                      :id="`purchase-${purchase.id}-btn`"
                      @click="
                        $toggleDropdown({
                          targetEl: `purchase-${purchase.id}-menu`,
                          triggerEl: `purchase-${purchase.id}-btn`,
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
                      :id="`purchase-${purchase.id}-menu`"
                      class="hidden z-10 w-[8rem] bg-white rounded shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800"
                      style="inset: 0px auto auto -300px !important"
                    >
                      <ul
                        class="py-1 text-sm font-normal text-gray-700 cursor-pointer divide-y divide-gray-300 dark:divide-gray-700"
                        aria-labelledby="dropdownDefault"
                      >
                        <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-gray-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'purchase-view',
                              params: { purchaseId: purchase.id },
                              query: { purchaseDate: purchaseDate },
                            })
                          "
                        >
                          <IconC
                            iconName="DocumentMagnifyingGlassIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("viewDocument") }}
                        </li>
                        <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-gray-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'purchase-edit',
                              params: { purchaseId: purchase.id },
                              query: { purchaseDate: purchaseDate },
                            })
                          "
                          v-if="$can('execute', 'purchases')"
                        >
                          <IconC
                            iconType="solid"
                            iconName="PencilIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("edit") }}
                        </li>
                        <li
                          class="inline-flex text-red-700 dark:text-red-600 flex-row gap-2 items-center py-2 px-4 hover:bg-gray-100 dark:hover:bg-neutral-700 w-full"
                          @click="deletePurchase(purchase)"
                          v-if="$can('execute', 'purchases')"
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
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getPurchases($event)"
    />
    <delete-modal
      :itemId="selectedPurchase.id"
      deleteAction="purchaseModule/deletePurchase"
      :title="$t('purchase')"
      deleteRef="delete-modal"
      @reload="getPurchases(currentPage)"
    >
    </delete-modal>
  </div>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
import HtmlToExcel from "@/services/mixins/HtmlToExcel";
export default {
  data() {
    return {
      isTableLoading: false,
      isExcelLoading: false,
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      allPurchases: [],
      selectedPurchase: [],
    };
  },
  components: {
    DeleteModal,
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

      let table = document.createElement("table");
      let thead = document.createElement("thead");
      let tbody = document.createElement("tbody");

      let headTr = document.createElement("tr");

      let idTh = document.createElement("th");
      idTh.innerHTML = "ID";
      headTr.appendChild(idTh);

      let sellerNameTh = document.createElement("th");
      sellerNameTh.innerHTML = this.$t("sellerName");
      headTr.appendChild(sellerNameTh);

      let invoiceTh = document.createElement("th");
      invoiceTh.innerHTML = this.$t("invoiceNumber");
      headTr.appendChild(invoiceTh);

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

      for await (const element of this.allPurchases) {
        let bodyTr = document.createElement("tr");
        let idTd = document.createElement("td");
        idTd.innerHTML = element.id;
        bodyTr.appendChild(idTd);

        let sellerNameTd = document.createElement("td");
        sellerNameTd.innerHTML = element.sellerName;
        bodyTr.appendChild(sellerNameTd);

        let invoiceTd = document.createElement("td");
        invoiceTd.innerHTML = element.sellerInvoiceNumber;
        bodyTr.appendChild(invoiceTd);

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
      let fileName =
        this.purchaseDate.replaceAll(".", "-") + `-${this.$t("purchases")}`;
      this.tableToExcel(table, fileName);
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
      this.$putOnFocus("delete-item-modal-btn");
    },
  },
};
</script>
