<template>
  <div
    :id="modalRef"
    :ref="modalRef"
    tabindex="-1"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full"
  >
    <div class="relative p-4 w-full max-w-md h-full md:h-auto">
      <div class="relative bg-white rounded shadow dark:bg-neutral-700">
        <div
          class="text-gray-700 dark:text-gray-200 flex justify-between items-center p-2.5"
        >
          <p class="text-xl">{{ actionTitle }} {{ actionText }}</p>
          <button
            type="button"
            class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-800/50"
            @click="$hideModal(modalRef)"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
            <span class="sr-only">Close modal</span>
          </button>
        </div>
        <div class="p-6 text-center">
          <IconC
            iconName="ExclamationCircleIcon"
            iconClass="mx-auto mb-4 w-14 h-14 text-gray-400 dark:text-gray-200"
          />
          <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            {{ $t("areYouSureTo", { action: actionTitle.toLowerCase() }) }}
          </h3>
          <button
            @click="$hideModal(modalRef)"
            :disabled="isLoading"
            type="button"
            class="gray-outline-btn mr-2 h-10 w-20 inline-flex items-center justify-center"
          >
            {{ $t("cancel") }}
          </button>
          <button
            @click="$emit('submit')"
            id="deactivate-item-modal-btn"
            type="button"
            class="red-gradient-btn h-10 w-20 inline-flex justify-center items-center"
          >
            <div role="status" v-if="isLoading">
              <IconC
                iconType="custom"
                iconName="SpinnerIcon"
                iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-red-600"
              />
              <span class="sr-only">Loading...</span>
            </div>
            <span v-else>{{ actionTitle }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modalRef: { type: String, required: true, default: "deactivate-modal" },
    actionTitle: { type: String, required: true, default: "Deactivate" },
    actionText: { type: String, required: true, default: "Object" },
    isLoading: { type: Boolean, required: true, default: false },
  },
};
</script>
