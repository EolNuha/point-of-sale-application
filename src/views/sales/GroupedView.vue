<!-- eslint-disable no-undef -->
<template>
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
            </template>
          </div>
        </th>
        <th
          scope="col"
          class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
          v-for="item in taxes"
          :key="item.settingsValue"
        >
          {{ $t("tax") }} {{ item.settingsName }}%
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
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
          <td class="py-2 px-6">
            {{ sale.dateCreated?.substring(0, 10) }}
          </td>
          <td class="py-2 px-6" v-for="item in taxes" :key="item.settingsValue">
            {{
              Array.isArray(sale.taxes)
                ? sale.taxes?.find((obj) => obj.taxAlias === item.settingsAlias)
                    ?.taxValue || "0.00"
                : "0.00"
            }}
            €
          </td>
          <td class="py-2 px-6">{{ sale.subTotalAmount }} €</td>
          <td class="py-2 px-6">{{ sale.totalAmount }} €</td>
          <td class="py-2 px-6">{{ sale.grossProfitAmount }} €</td>
          <td class="py-2 px-6">{{ sale.netProfitAmount }} €</td>
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
              class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
            >
              <IconC
                iconName="DocumentMagnifyingGlassIcon"
                iconClass="h-5 w-5 text-gray-900 dark:text-gray-300"
              />
            </button>
          </td>
        </tr>
      </template>
      <tr
        v-if="sales?.length !== 0"
        class="text-md uppercase font-bold bg-white border-b dark:bg-neutral-900 dark:border-gray-700"
      >
        <td class="py-4 px-6">{{ $t("total") }}</td>
        <td
          class="py-2 px-6"
          v-for="item in pagination.taxes"
          :key="item.settingsValue"
        >
          {{ Number(item.taxValue).toFixed(2) }} €
        </td>
        <td class="py-4 px-6">{{ pagination.salesSubTotalAmount }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalAmount }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalGrossProfit }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalNetProfit }} €</td>
        <td class="py-4 px-6"></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: ["sales", "taxes", "pagination"],
  data() {
    return {
      sortColumn: null,
      sortDir: "desc",
    };
  },
  methods: {
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.$emit("sort", col);
    },
    deletePurchase(purchase) {
      this.selectedPurchase = purchase;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
  },
};
</script>
