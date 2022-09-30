<template>
  <div class="flex flex-col bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="bg-white dark:bg-gray-900 rounded-3xl py-8 relative px-10">
      <OverlayC v-if="isLoading" />
      <h2 class="text-gray-700 dark:text-gray-300 text-3xl font-extrabold">
        Purchase #{{ $route.params.purchaseId }}
      </h2>
      <div class="flex flex-row pt-5">
        <div class="basis-3/4 md:basis-1/2 lg:basis-1/4">
          <table class="text-gray-700 dark:text-gray-400 text-sm w-full">
            <tbody>
              <tr>
                <td class="py-2">Seller name</td>
                <td class="text-right py-2">{{ purchase.sellerName }}</td>
              </tr>
              <tr>
                <td class="py-2">Invoice number</td>
                <td class="text-right py-2">
                  {{ purchase.sellerInvoiceNumber }}
                </td>
              </tr>
              <tr>
                <td class="py-2">Fiscal number</td>
                <td class="text-right py-2">
                  {{ purchase.sellerFiscalNumber }}
                </td>
              </tr>
              <tr>
                <td class="py-2">Tax number</td>
                <td class="text-right py-2">
                  {{ purchase.sellerTaxNumber }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style">
        <table
          class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative my-5"
        >
          <thead
            class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
          >
            <tr>
              <th scope="col" class="py-3 px-6">ID</th>
              <th scope="col" class="py-3 px-6">Name</th>
              <th scope="col" class="py-3 px-6">Barcode</th>
              <th scope="col" class="py-3 px-6">Stock</th>
              <th scope="col" class="py-3 px-6">Purchased Price</th>
              <th scope="col" class="py-3 px-6">Price w/o Tax</th>
              <th scope="col" class="py-3 px-6">Tax</th>
              <th scope="col" class="py-3 px-6">Selling Price</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in purchase.purchaseItems" :key="item.id">
              <tr class="bg-white dark:bg-gray-900">
                <td class="py-3 px-6">{{ item.product.id }}</td>
                <td
                  class="py-3 px-6 text-black dark:text-white cursor-pointer"
                  @click="
                    $router.push({
                      name: 'product-view',
                      params: { productId: item.product.id },
                    })
                  "
                >
                  {{ item.product.name }}
                </td>
                <td class="py-3 px-6">{{ item.product.barcode }}</td>
                <td class="py-3 px-6">x {{ item.product.stock }}</td>
                <td class="py-3 px-6 max-w-xs break-words">
                  {{ item.product.purchasedPrice }} €
                </td>
                <td class="py-3 px-6 max-w-xs break-words">
                  {{ item.priceWithoutTax }} €
                </td>
                <td class="py-3 px-6 max-w-xs break-words">
                  {{ item.taxAmount }} € ({{ item.product.tax }}%)
                </td>
                <td class="py-3 px-6 max-w-xs break-words">
                  {{ item.product.sellingPrice }} €
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <hr class="border-gray-500" />
      </div>
      <div class="flex flex-row justify-end p-5">
        <div class="basis-3/4 md:basis-1/2 lg:basis-1/4">
          <table class="text-gray-700 dark:text-gray-300 w-full">
            <tbody>
              <tr>
                <td class="py-2">SUBTOTAL</td>
                <td class="text-right py-2">{{ purchase.subTotalAmount }} €</td>
              </tr>
              <tr v-if="purchase.eightTaxAmount > 0">
                <td class="py-2">TAX RATE (8%)</td>
                <td class="text-right py-2">{{ purchase.eightTaxAmount }} €</td>
              </tr>
              <tr v-if="purchase.eighteenTaxAmount > 0">
                <td class="py-2">TAX RATE (18%)</td>
                <td class="text-right py-2">
                  {{ purchase.eighteenTaxAmount }} €
                </td>
              </tr>
              <tr class="font-bold text-xl">
                <td class="py-2">TOTAL</td>
                <td class="text-right py-2">{{ purchase.totalAmount }} €</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoading: true,
    };
  },
  computed: {
    purchase() {
      return this.$store.state.purchaseModule.purchase;
    },
  },
  async mounted() {
    await this.$store
      .dispatch(
        "purchaseModule/getPurchaseDetails",
        this.$route.params.purchaseId
      )
      .then(() => {
        this.isLoading = false;
      });
  },
};
</script>
