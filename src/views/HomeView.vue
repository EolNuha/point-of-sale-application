<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <form class="flex items-center w-64">
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
          type="text"
          id="simple-search"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Search"
          required
        />
      </div>
      <button
        type="submit"
        class="p-2.5 ml-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <IconC iconName="Search" iconClass="w-5 h-5" />
        <span class="sr-only">Search</span>
      </button>
    </form>

    <div class="overflow-x-auto relative shadow-md sm:rounded-lg my-5">
      <table
        class="w-full text-sm text-left text-gray-500 dark:text-gray-400 relative"
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
          </tr>
        </thead>
        <tbody>
          <tr
            class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 cursor-pointer hover:opacity-75"
            v-for="product in $store.state.products"
            :key="product.id"
            @click="
              $router.push({
                name: 'product-view',
                params: { productId: product.id },
              })
            "
          >
            <th
              scope="row"
              class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {{ product.id }}
            </th>
            <td class="py-4 px-6">{{ product.name }}</td>
            <td class="py-4 px-6">{{ product.description }}</td>
            <td class="py-4 px-6">{{ product.price }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "HomeView",
  data() {
    return {
      isLoading: false,
    };
  },
  created() {
    this.isLoading = true;
    this.$store.dispatch("getProducts").then(() => {
      this.isLoading = false;
    });
  },
};
</script>
