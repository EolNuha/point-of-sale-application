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
            @click="$hideModal(deleteRef)"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <div class="p-6 text-center">
          <IconC :iconName="icon.name" :iconClass="icon.class" />
          <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Are you sure you want to delete this?
          </h3>
          <button
            @click="$hideModal(deleteRef)"
            :disabled="isLoading"
            type="button"
            class="gray-outline-btn mr-2 h-10 w-20 inline-flex items-center justify-center"
          >
            Cancel
          </button>
          <button
            @click="deleteFunc"
            type="button"
            class="red-gradient-btn h-10 w-20 inline-flex justify-center items-center"
          >
            <IconC
              v-if="isLoading"
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-red-600"
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
        name: "ExclamationCircleIcon",
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
    deleteFunc() {
      this.isLoading = true;
      this.$store
        .dispatch(this.deleteAction, this.productId)
        .then(() => {
          this.$toast.success(`${this.title} deleted successfully!`);
          this.$emit("reload");
          this.$hideModal(this.deleteRef);
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
