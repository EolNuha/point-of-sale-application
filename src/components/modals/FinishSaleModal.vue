<template>
  <div
    :id="modalRef"
    :ref="modalRef"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 w-full md:inset-0 h-modal md:h-full"
  >
    <div class="relative p-4 w-full max-w-md h-full md:h-auto">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-neutral-700">
        <button
          type="button"
          class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-neutral-800 dark:hover:text-white"
          @click="$hideModal(modalRef)"
          :disabled="isLoading"
        >
          <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
          <span class="sr-only">Close modal</span>
        </button>
        <div class="py-6 px-6 lg:px-8">
          <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
            {{ $t("finishSale") }}
          </h3>
          <Form
            v-slot="{ errors }"
            @submit="$emit('submit', customerAmount)"
            class="space-y-6"
          >
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ $t("saleTotal") }}</label
              >
              <input
                :value="total"
                type="number"
                name="sale_total"
                id="sale_total"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-neutral-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                placeholder="Sale total"
                disabled
              />
              <span class="text-red-700">{{ errors.sale_total }}</span>
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ $t("customerAmount") }}</label
              >
              <Field
                :rules="isRequired"
                v-model="customerAmount"
                @focus="$event.target.select()"
                type="number"
                name="customer_amount"
                id="customer_amount"
                ref="customer_amount"
                step="0.01"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-neutral-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                :placeholder="$t('customerAmount')"
                required
                :disabled="isLoading"
              />
              <span class="text-red-700">{{ errors.customer_amount }}</span>
            </div>
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                {{ $t("changeAmount") }}</label
              >
              <Field
                :rules="isChangeAmountValid"
                v-model="changeAmount"
                type="number"
                name="change_amount"
                id="change_amount"
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 dark:bg-neutral-600 dark:border-gray-500 dark:text-white"
                :placeholder="$t('changeAmount')"
                disabled
              />
              <span class="text-red-700">{{ errors.change_amount }}</span>
            </div>
            <button
              id="finish-sale-modal-btn"
              type="submit"
              class="inline-flex items-center justify-center w-full blue-gradient-btn"
            >
              <div role="status" v-if="isLoading">
                <IconC
                  iconType="custom"
                  iconName="SpinnerIcon"
                  iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
                />
                <span class="sr-only">Loading...</span>
              </div>
              <template v-else>{{ $t("finishSale") }}</template>
            </button>
          </Form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";
export default {
  components: {
    Field,
    Form,
  },
  props: {
    total: { type: null, required: true, default: null },
    isLoading: { type: null, required: true, default: false },
    modalRef: { type: String, required: true, default: "sale-modal" },
  },
  data() {
    return {
      customerAmount: "0.00",
      changeAmount: "0.00",
    };
  },
  watch: {
    total: {
      async handler(value) {
        this.customerAmount = value;
      },
    },
    customerAmount: {
      async handler(value) {
        this.changeAmount = (value - this.total).toFixed(2);
      },
    },
  },
  methods: {
    isRequired(value) {
      return value ? true : this.$t("isRequired");
    },
    isChangeAmountValid() {
      const value = this.customerAmount - this.total;
      if (value >= 0) {
        return true;
      } else {
        return this.$t("changeAmountLessThanZero");
      }
    },
  },
};
</script>
