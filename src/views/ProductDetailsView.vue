<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen">
    <Form v-slot="{ errors }" class="p-5" @submit="updateProduct">
      <div class="mb-6">
        <label
          for="product_name"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
          >Product Name</label
        >
        <Field
          name="product_name"
          :rules="isRequired"
          v-model="product.name"
          type="text"
          id="product_name"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Enter product eol"
          required
        />
        <span class="text-red-700">{{ errors.product_name }}</span>
      </div>
      <div class="mb-6">
        <label
          for="product_description"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400"
          >Product Description</label
        >
        <Field
          as="textarea"
          name="product_description"
          v-model="product.description"
          id="product_description"
          rows="4"
          class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Product description..."
          required
        />
        <span class="text-red-700">{{ errors.product_description }}</span>
      </div>
      <div class="mb-6">
        <label
          for="product_price"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
          >Product Price</label
        >
        <Field
          name="product_price"
          :rules="isRequired"
          v-model="product.price"
          type="number"
          step="any"
          id="product_price"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Enter product price"
          required
        />
        <span class="text-red-700">{{ errors.product_price }}</span>
      </div>
      <div class="mb-6">
        <label
          for="product_price"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
          >Date Created</label
        >
        <input
          name="product_price"
          v-model="product.dateCreated"
          type="any"
          step="any"
          id="product_price"
          class="disabled bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Enter product price"
          disabled
        />
      </div>
      <div class="mb-6">
        <label
          for="product_price"
          class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
          >Last Modified</label
        >
        <input
          name="product_price"
          v-model="product.dateModified"
          type="any"
          step="any"
          id="product_price"
          class="disabled bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          disabled
        />
      </div>

      <button
        type="submit"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-32 px-5 py-1.5 flex justify-center items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <div role="status" v-if="isLoading">
          <IconC
            iconType="custom"
            iconName="SpinnerIcon"
            iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
          />
          <span class="sr-only">Loading...</span>
        </div>
        <div v-else>Update</div>
      </button>
    </Form>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";

export default {
  name: "ProductDetailsView",
  components: {
    Field,
    Form,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  computed: {
    product() {
      return this.$store.state.productModule.product;
    },
  },
  async mounted() {
    await this.$store
      .dispatch("productModule/getProductDetails", this.$route.params.productId)
      .then(async (response) => {
        this.$route.meta.title = response.data.name;
      });
  },
  methods: {
    isRequired(value) {
      return value ? true : "This field is required";
    },
    updateProduct() {
      this.isLoading = true;
      const data = {
        id: this.product.id,
        name: this.product.name,
        description: this.product.description,
        price: this.product.price,
      };
      this.$store
        .dispatch("productModule/updateProduct", data)
        .then((response) => {
          this.isLoading = false;
          console.log(response.data);
          this.$toast.success("Product updated successfully!");
        })
        .catch(() => {
          this.isLoading = false;
          this.$toast.error("Something went wrong!");
        });
    },
  },
};
</script>
