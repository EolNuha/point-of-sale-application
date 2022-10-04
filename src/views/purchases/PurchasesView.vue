<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2">
        <select
          v-model="currentMonth"
          class="w-[120px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full px-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option v-for="(month, index) in months" :key="month" :value="index">
            {{ month }}
          </option>
        </select>

        <div class="flex items-center gap-2">
          <input
            v-model="startDate"
            ref="startDate"
            name="start"
            type="date"
            class="w-[9.3rem] bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block px-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Select date start"
            :max="endDate"
          />
          <span class="text-gray-500">to</span>
          <input
            v-model="endDate"
            ref="endDate"
            name="start"
            type="date"
            class="w-[9.3rem] bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block px-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Select date end"
            :min="startDate"
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
          class="blue-gradient-btn inline-flex items-center text-center"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
          New Purchase
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

    <div
      class="overflow-x-auto relative sm:rounded-xl my-5 scrollbar-style min-h-65"
    >
      <table
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <OverlayC v-if="isTableLoading" />
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6">Date</th>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Total Amount</th>
            <th scope="col" class="py-3 px-6">Seller Name</th>
            <th scope="col" class="py-3 px-6">Seller Invoice Number</th>
            <th scope="col" class="py-3 px-6"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="purchase in purchases" :key="purchase.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <td class="py-2 px-6">
                {{ purchase.dateCreated.substring(0, 10) }}
              </td>
              <td class="py-2 px-6">{{ purchase.id }}</td>
              <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
              <td class="py-2 px-6">{{ purchase.sellerName }}</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ purchase.sellerInvoiceNumber }}
              </td>
              <td class="py-2 px-6">
                <button
                  @click="
                    $router.push({
                      name: 'purchase-view',
                      params: { purchaseId: purchase.id },
                    })
                  "
                  class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
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
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getPurchases($event)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isTableLoading: false,
      currentPage: 1,
      searchQuery: "",
      isExcelLoading: false,
      excelSales: [],
      months: [
        "Custom",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ],
      monthDates: [],
      currentMonth: "",
      startDate: "",
      endDate: "",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("purchaseModule/getPurchases", {
            page: this.currentPage,
            search: value,
          });
          this.isTableLoading = false;
        } catch {
          this.isTableLoading = false;
        }
      },
    },
    currentMonth: {
      async handler(value) {
        if (value !== 0) {
          const month = String(value).padStart(2, "0");
          const year = new Date().getFullYear();
          const days = String(new Date(year, month, 0).getDate()).padStart(
            2,
            "0"
          );
          this.startDate = `${year}-${month}-01`;
          this.endDate = `${year}-${month}-${days}`;
        }
      },
    },
    startDate: {
      async handler(value) {
        this.isTableLoading = true;
        const idx = this.checkIfMonth(value, this.endDate);
        if (idx !== -1) {
          this.currentMonth = idx + 1;
        } else {
          this.currentMonth = 0;
        }
        this.$store
          .dispatch("purchaseModule/getPurchases", {
            startDate: value,
            endDate: this.endDate,
            page: this.currentPage,
          })
          .then(() => {
            this.isTableLoading = false;
          })
          .catch(() => {
            this.isTableLoading = false;
            this.$toast.error("Something went wrong, please try again later!");
          });
      },
    },
    endDate: {
      async handler(value) {
        this.isTableLoading = true;
        const idx = this.checkIfMonth(this.startDate, value);
        if (idx !== -1) {
          this.currentMonth = idx + 1;
        } else {
          this.currentMonth = 0;
        }
        this.$store
          .dispatch("purchaseModule/getPurchases", {
            startDate: this.startDate,
            endDate: value,
            page: this.currentPage,
          })
          .then(() => {
            this.isTableLoading = false;
          })
          .catch(() => {
            this.isTableLoading = false;
            this.$toast.error("Something went wrong, please try again later!");
          });
      },
    },
  },
  created() {
    const currentMonth = this.getMonth(new Date().getMonth() + 1);
    this.currentMonth = new Date().getMonth() + 1;
    this.startDate = currentMonth.startDate;
    this.endDate = currentMonth.endDate;
    for (let i = 0; i < this.months.length; i++) {
      this.monthDates.push(this.getMonth(i + 1));
    }
    this.reload();
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
    reload() {
      this.isTableLoading = true;
      this.selectedProduct = {};
      this.$store
        .dispatch("purchaseModule/getPurchases", {
          page: this.currentPage,
          startDate: this.startDate,
          endDate: this.endDate,
        })
        .then(() => {
          this.isTableLoading = false;
        })
        .catch(() => {
          this.$toast.error("Something went wrong, please try again later!");
        });
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
    checkIfMonth(start, end) {
      return this.monthDates.findIndex(
        (el) => el.startDate === start && el.endDate === end
      );
    },
    getPurchases(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("purchaseModule/getPurchases", {
          page: page,
          startDate: this.startDate,
          endDate: this.endDate,
        })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    async downloadExcel() {
      this.isExcelLoading = true;
      let fileName;
      const idx = this.checkIfMonth(this.startDate, this.endDate);
      if (idx !== -1) {
        fileName = `${this.months[idx + 1]}-${this.startDate.substring(0, 4)}`;
      } else {
        fileName = `${this.startDate}-TO-${this.endDate}`;
      }
      let purchases;
      await this.$store
        .dispatch("purchaseModule/getPurchasesForExcel", {
          startDate: this.startDate,
          endDate: this.endDate,
          page: this.currentPage,
          per_page: this.pagination.total,
        })
        .then((res) => {
          purchases = res.data.data;
        });
      const data = {
        fileName: fileName,
        purchases: purchases,
      };
      this.$store
        .dispatch("purchaseModule/downloadExcelFile", data)
        .then(() => {
          this.isExcelLoading = false;
          this.$toast.success(
            "Excel file downloaded successfully! You can find the file in the Downloads folder."
          );
        })
        .catch(() => {
          this.isExcelLoading = false;
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
  },
};
</script>
