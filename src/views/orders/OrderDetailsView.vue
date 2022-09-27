<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <p class="text-gray-700 dark:text-gray-300 text-5xl">
      Order #{{ $route.params.orderId }}
    </p>
    <div
      class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style mb-[8.5rem]"
    >
      <table
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Product name</th>
            <th scope="col" class="py-3 px-6">Barcode</th>
            <th scope="col" class="py-3 px-6">Quantity</th>
            <th scope="col" class="py-3 px-6">Selling Price</th>
            <th scope="col" class="py-3 px-6">Total</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="item in order.orderItems" :key="item.id">
            <tr
              class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
            >
              <td class="py-2 px-6">
                {{ item.product.id }}
              </td>
              <td class="py-2 px-6">{{ item.product.name }}</td>
              <td class="py-2 px-6">{{ item.product.barcode }}</td>
              <td class="py-2 px-6">x {{ item.quantity }}</td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ item.product.sellingPrice }} €
              </td>
              <td class="py-2 px-6 max-w-xs break-words">
                {{ (item.product.sellingPrice * item.quantity).toFixed(2) }} €
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div
      class="fixed bottom-0 left-[16rem] right-0 flex items-center justify-end h-16 bg-gray-100 dark:bg-gray-700 p-2"
    >
      <div
        class="flex flex-row items-center text-5xl text-gray-700 dark:text-gray-300"
      >
        Total:
        <div
          class="min-w-64 max-w-md h-14 ml-3 flex items-center justify-center p-2.5 bg-gray-200 dark:bg-gray-800 rounded-lg"
        >
          <span id="total">{{ order.totalAmount }}</span
          >€
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    order() {
      return this.$store.state.orderModule.order;
    },
  },
  async mounted() {
    await this.$store.dispatch(
      "orderModule/getOrderDetails",
      this.$route.params.orderId
    );
  },
};
</script>
