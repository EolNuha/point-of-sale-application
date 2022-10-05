<template>
  <div
    class="absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center min-h-65"
  >
    <IconC iconName="NoSymbolIcon" iconClass="w-12 h-12" />
    <h2 class="text-gray-700 dark:text-gray-300 text-2xl my-4">
      {{
        search
          ? `No ${pluralText.toLowerCase()} have been found...`
          : `No ${pluralText.toLowerCase()} have been added yet...`
      }}
    </h2>
    <button
      @click="
        $router.push({
          name: `${routeName}`,
        })
      "
      class="relative inline-flex items-center justify-center"
      :class="btnClass"
    >
      <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
      Add New {{ singularText }}
    </button>
  </div>
</template>
<script>
export default {
  props: {
    pluralText: {
      type: String,
      required: false,
    },
    singularText: {
      type: String,
      required: false,
    },
    btnClass: {
      type: String,
      required: false,
      default: "blue-gradient-btn",
    },
    routeName: {
      type: String,
      required: false,
    },
    search: {
      type: String,
      required: false,
    },
  },
};
</script>
