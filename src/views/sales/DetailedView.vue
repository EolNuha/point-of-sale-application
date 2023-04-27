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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
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
          <td class="py-2 px-6">{{ sale.dateCreated?.substring(0, 10) }}</td>
          <td class="py-2 px-6">
            {{ sale.user?.firstName }} {{ sale.user?.lastName }}
          </td>
          <td class="py-2 px-6">
            {{ sale.isRegular ? $t("regular") : $t("irregular") }}
          </td>
          <td class="py-2 px-6" v-for="item in taxes" :key="item.settingsValue">
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
                      query: {
                        saleDate: sale.dateCreated?.substring(0, 10),
                      },
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
                      query: {
                        saleDate: sale.dateCreated?.substring(0, 10),
                      },
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
        <td class="py-4 px-6">{{ pagination.salesSubTotalAmount }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalAmount }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalGrossProfit }} €</td>
        <td class="py-4 px-6">{{ pagination.salesTotalNetProfit }} €</td>
        <td class="py-4 px-6"></td>
      </tr>
    </tbody>
    <delete-modal
      :itemId="selectedSale.id"
      deleteAction="saleModule/deleteSale"
      :title="$t('sale')"
      deleteRef="delete-modal"
      @reload="$emit('reload', true)"
    >
    </delete-modal>
  </table>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
export default {
  props: ["sales", "taxes", "pagination"],
  data() {
    return {
      sortColumn: null,
      sortDir: "desc",
      selectedSale: [],
    };
  },
  components: {
    DeleteModal,
  },
  methods: {
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.$emit("sort", col);
    },
    deleteSale(sale) {
      this.selectedSale = sale;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
  },
};
</script>
