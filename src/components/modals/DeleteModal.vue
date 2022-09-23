<template>
  <div
    :id="deleteRef"
    :ref="deleteRef"
    tabindex="-1"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full"
  >
    <div class="relative p-4 w-full max-w-md h-full md:h-auto">
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
        <div class="flex items-center p-2.5">
          <p class="text-gray-700 dark:text-gray-200 text-xl">
            Delete {{ title }}
          </p>
          <button
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
            @click="hideModal"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <div class="p-6 text-center">
          <IconC iconName="ExclamationCircleIcon" :iconClass="icon.class" />
          <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Are you sure you want to delete this?
          </h3>
          <button
            @click="hideModal"
            :disabled="isLoading"
            type="button"
            class="text-gray-500 bg-white w-20 h-10 hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 inline-flex items-center justify-center dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-600 mr-2"
          >
            Cancel
          </button>
          <button
            @click="deleteFunc"
            type="button"
            class="text-white bg-red-600 w-20 h-10 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 text-sm font-medium rounded-lg inline-flex items-center justify-center px-5 py-2.5"
          >
            <IconC
              v-if="isLoading"
              iconName="Spinner"
              iconClass="w-4 h-4 text-gray-200 animate-spin fill-gray-700"
            />
            <span v-else>Delete</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    productId: { type: null, required: true, default: null },
    deleteAction: {
      type: [Number, String, Object, Array],
      required: true,
      default: null,
    },
    getAction: {
      type: [Number, String, Object, Array],
      required: true,
      default: null,
    },
    deleteRef: { type: String, required: true, default: "delete-modal" },
    title: { type: String, required: true, default: "Object" },
    icon: {
      type: Object,
      required: false,
      default: () => ({
        name: "ExlamationCircle",
        class: "mx-auto mb-4 w-14 h-14 text-gray-400 dark:text-gray-200",
      }),
    },
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    hideModal() {
      const el = document.getElementById(this.deleteRef);
      // eslint-disable-next-line no-undef
      const mod = new Modal(el);
      mod.hide();
      document.querySelector("[modal-backdrop]").remove();
    },
    deleteFunc() {
      this.isLoading = true;
      this.$store
        .dispatch(this.deleteAction, this.productId)
        .then(() => {
          this.$toast.success(`${this.title} deleted successfully!`);
          this.$emit("reload");
          this.hideModal();
          this.isLoading = false;
        })
        .catch((error) => {
          this.isLoading = false;
          this.$toast.error(
            error.data || "Something went wrong, please try again later!"
          );
        });
    },
  },
};
</script>
