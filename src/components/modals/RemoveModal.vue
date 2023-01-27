<template>
  <div
    :id="removeRef"
    :ref="removeRef"
    tabindex="-1"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full"
  >
    <div class="relative p-4 w-full max-w-md h-full md:h-auto">
      <div class="relative bg-white rounded shadow dark:bg-neutral-700">
        <div
          class="text-gray-700 dark:text-gray-200 flex justify-between items-center p-2.5"
        >
          <p class="text-xl">{{ $t("remove") }} {{ $t("products") }}</p>
          <button
            type="button"
            class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-800/50"
            @click="$hideModal(removeRef)"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <div class="p-6 text-center">
          <IconC :iconName="icon.name" :iconClass="icon.class" />
          <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            {{ $t("areYouSureToRemove") }}
          </h3>
          <div class="flex items-center justify-center gap-2">
            <button
              @click="$hideModal(removeRef)"
              :disabled="isLoading"
              type="button"
              class="gray-outline-btn h-10 w-20 inline-flex items-center justify-center"
            >
              {{ $t("cancel") }}
            </button>
            <button
              @click="$emit('remove', value)"
              :id="removeRef + '_remove_btn'"
              :ref="removeRef + '_remove_btn'"
              type="button"
              class="red-gradient-btn h-10 w-20 inline-flex justify-center items-center"
            >
              <IconC
                v-if="isLoading"
                iconType="custom"
                iconName="SpinnerIcon"
                iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-red-600"
              />
              <span v-else>{{ $t("remove") }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    value: { type: Array, required: true },
    removeRef: { type: String, required: true, default: "remove-modal" },
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
};
</script>
