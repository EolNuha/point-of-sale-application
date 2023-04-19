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
        <template v-for="item in taxes" :key="item.settingsValue">
          <th
            scope="col"
            class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
          >
            {{ item.settingsName }}%
          </th>
          <th
            scope="col"
            class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600 cursor-not-allowed"
          >
            {{ $t("subTotal") }} {{ item.settingsName }}%
          </th>
        </template>
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
        <th scope="col" class="py-3 px-6"></th>
      </tr>
    </thead>
    <tbody>
      <template v-for="purchase in purchases" :key="purchase.id">
        <tr
          class="bg-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:bg-neutral-100/75 dark:hover:bg-neutral-900/[.5]"
        >
          <td class="py-2 px-6">
            {{ purchase.dateCreated?.substring(0, 10) }}
          </td>
          <template v-for="item in taxes" :key="item.settingsValue">
            <td class="py-2 px-6">
              {{
                Array.isArray(purchase.taxes)
                  ? purchase.taxes?.find(
                      (obj) => obj.taxAlias === item.settingsAlias
                    )?.taxValue || "0.00"
                  : "0.00"
              }}
              €
            </td>
            <td class="py-2 px-6">
              {{
                Array.isArray(purchase.taxes)
                  ? purchase.taxes?.find(
                      (obj) => obj.taxAlias === item.settingsAlias
                    )?.totalWithoutTax || "0.00"
                  : "0.00"
              }}
              €
            </td>
          </template>
          <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
          <td class="py-2 px-6">
            <button
              @click="
                $router.push({
                  name: 'daily-purchases',
                  query: {
                    purchaseDate: purchase.dateCreated?.substring(0, 10),
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
    </tbody>
  </table>
</template>

<script>
export default {
  props: ["purchases", "taxes"],
  data() {
    return {
      sortColumn: null,
      sortDir: "desc",
      selectedPurchase: [],
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
