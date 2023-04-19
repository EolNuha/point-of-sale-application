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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
            </template>
          </div>
        </th>
        <th
          scope="col"
          class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
              <IconC iconName="ArrowLongUpIcon" iconClass="w-4 h-4" v-else />
            </template>
          </div>
        </th>
        <th
          scope="col"
          class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
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
          <td class="py-2 px-6">{{ purchase.id }}</td>
          <td class="py-2 px-6">{{ purchase.sellerName }}</td>
          <td class="py-2 px-6">{{ purchase.sellerInvoiceNumber }}</td>
          <template v-for="item in taxes" :key="item.settingsValue">
            <td class="py-2 px-6">
              {{
                purchase.taxes
                  ? purchase.taxes[item.settingsAlias]?.taxValue || "0.00"
                  : "0.00"
              }}
              €
            </td>
            <td class="py-2 px-6">
              {{
                purchase.taxes
                  ? purchase.taxes[item.settingsAlias]?.totalWithoutTax ||
                    "0.00"
                  : "0.00"
              }}
              €
            </td>
          </template>
          <td class="py-2 px-6">{{ purchase.totalAmount }} €</td>
          <td class="py-2 px-6 w-1.5" v-if="$can('read', 'purchases')">
            <button
              class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
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
                  class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                  @click="
                    $router.push({
                      name: 'purchase-view',
                      params: { purchaseId: purchase.id },
                      query: {
                        purchaseDate: purchase.dateCreated?.substring(0, 10),
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
                      name: 'purchase-edit',
                      params: { purchaseId: purchase.id },
                      query: {
                        purchaseDate: purchase.dateCreated?.substring(0, 10),
                      },
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
                </li> -->
                <li
                  class="inline-flex text-red-700 dark:text-red-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
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
    <delete-modal
      :itemId="selectedPurchase.id"
      deleteAction="purchaseModule/deletePurchase"
      :title="$t('purchase')"
      deleteRef="delete-modal"
      @reload="$emit('reload', true)"
    >
    </delete-modal>
  </table>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
export default {
  props: ["purchases", "taxes"],
  data() {
    return {
      sortColumn: null,
      sortDir: "desc",
      selectedPurchase: [],
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
    deletePurchase(purchase) {
      this.selectedPurchase = purchase;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-modal-btn");
    },
  },
};
</script>
