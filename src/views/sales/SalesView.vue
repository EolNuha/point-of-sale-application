<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <select
          v-model="currentMonth"
          class="w-[120px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        >
          <option v-for="month in months" :key="month" :value="month">
            {{ month }}
          </option>
        </select>
      </div>
      <div>
        <button
          @click="
            $router.push({
              name: 'new-sale',
            })
          "
          class="blue-gradient-btn inline-flex items-center text-center mr-2"
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
    <div
      class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style min-h-65"
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
            <th scope="col" class="py-3 px-6">8%</th>
            <th scope="col" class="py-3 px-6">18%</th>
            <th scope="col" class="py-3 px-6">Subtotal Amount</th>
            <th scope="col" class="py-3 px-6">Total Amount</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="sale in sales" :key="sale.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <td class="py-2 px-6">{{ sale.dateCreated }}</td>
              <td class="py-2 px-6">{{ sale.eightTaxAmount }} €</td>
              <td class="py-2 px-6">{{ sale.eighteenTaxAmount }} €</td>
              <td class="py-2 px-6">{{ sale.subTotalAmount }} €</td>
              <td class="py-2 px-6">{{ sale.totalAmount }} €</td>
            </tr>
          </template>
        </tbody>
      </table>
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
      selectedProduct: {},
      selectedProductToDelete: {},
      currentPage: 1,
      searchQuery: "",
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
      currentMonth: "",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("saleModule/getSales", {
            page: this.currentPage,
            search: value,
            month: this.currentMonth,
          });
          this.isTableLoading = false;
        } catch {
          this.isTableLoading = false;
        }
      },
    },
    currentMonth: {
      async handler(value) {
        this.isTableLoading = true;
        try {
          await this.$store.dispatch("saleModule/getSales", {
            page: this.currentPage,
            month: value,
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
  },
  created() {
    this.currentMonth = this.months[new Date().getMonth() + 1];
    this.reload();
  },
  methods: {
    reload() {
      this.isTableLoading = true;
      this.selectedProduct = {};
      this.$store
        .dispatch("saleModule/getSales", {
          month: this.currentMonth,
          page: this.currentPage,
        })
        .then((res) => {
          this.isTableLoading = false;
          this.excelSales = res.data.data;
        })
        .catch(() => {
          this.$toast.error("Something went wrong, please try again later!");
        });
    },
    getSales(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("saleModule/getSales", {
          page: page,
          month: this.currentMonth,
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
      let sales;
      await this.$store
        .dispatch("saleModule/getSalesForExcel", {
          month: this.currentMonth,
          page: this.currentPage,
          per_page: this.pagination.total,
        })
        .then((res) => {
          sales = res.data.data;
        });
      const data = {
        month: this.currentMonth,
        sales: sales,
      };
      this.isExcelLoading = true;
      this.$store
        .dispatch("saleModule/downloadExcelFile", data)
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
