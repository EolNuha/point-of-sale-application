<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="flex items-center justify-between">
      <button
        @click="
          $router.push({
            name: 'products-create',
          })
        "
        class="flex items-center text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-auto px-5 py-1.5 flex justify-center items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <IconC iconName="Plus" iconClass="w-5 h-5 mr-2" /> Create Product
      </button>
      <div class="flex items-center w-64">
        <label for="simple-search" class="sr-only">Search</label>
        <div class="relative w-full">
          <div
            class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none"
          >
            <IconC
              iconName="Search"
              iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
            />
          </div>
          <input
            v-model="search"
            type="text"
            id="simple-search"
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-1.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search"
            required
          />
        </div>
      </div>
    </div>

    <div class="overflow-x-auto relative sm:rounded-lg my-5 scrollbar-style">
      <table
        v-if="products.length"
        class="w-full text-sm text-left text-gray-700 dark:text-gray-400 relative"
      >
        <OverlayC v-if="isLoading" />
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Product name</th>
            <th scope="col" class="py-3 px-6">Description</th>
            <th scope="col" class="py-3 px-6">Price</th>
            <th scope="col" class="py-3 px-6"></th>
            <th scope="col" class="py-3 px-6"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:opacity-75"
            v-for="product in $store.state.products"
            :key="product.id"
          >
            <th
              scope="row"
              class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {{ product.id }}
            </th>
            <td class="py-4 px-6">{{ product.name }}</td>
            <td class="py-4 px-6 max-w-xs break-words">
              {{ product.description }}
            </td>
            <td class="py-4 px-6">{{ product.price }} $</td>
            <td
              class="py-4 px-6"
              @click="
                $router.push({
                  name: 'product-view',
                  params: { productId: product.id },
                })
              "
            >
              <IconC
                iconName="Pencil"
                iconClass="w-5 h-5 text-blue-700 cursor-pointer hover:text-blue-500 rounded-full"
              />
            </td>
            <td class="py-4 px-6" @click="deleteProduct(product.id)">
              <IconC
                iconName="Trash"
                iconClass="w-5 h-5 text-red-700 cursor-pointer hover:text-red-500"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      isLoading: false,
      search: "",
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    products() {
      return this.$store.state.products;
    },
  },
  created() {
    this.isLoading = true;
    this.$store.dispatch("getProducts").then(() => {
      this.isLoading = false;
    });
  },
  methods: {
    deleteProduct(productId) {
      this.$store
        .dispatch("deleteProduct", productId)
        .then(() => {
          this.$toast.success("Product deleted successfully!");
          this.$store.dispatch("getProducts");
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error(
            error.data || "Something went wrong, please try again later!"
          );
        });
    },
  },
};
</script>
