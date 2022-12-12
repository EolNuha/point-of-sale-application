<template>
  <div
    class="absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center text-gray-700 dark:text-gray-300"
    :class="minHeight"
  >
    <IconC iconName="NoSymbolIcon" iconClass="w-12 h-12" v-if="!search" />
    <IconC iconName="MagnifyingGlassIcon" iconClass="w-12 h-12" v-else />
    <h2 class="text-2xl my-4">
      {{
        search
          ? $t("noResultsFound", {
              result: $t(singularText.toLowerCase()).toLowerCase(),
            })
          : $t("noResultsAdded", {
              result: $t(singularText.toLowerCase()).toLowerCase(),
            })
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
      {{
        $t("addNewResult", {
          result: $t(singularText.toLowerCase()).toLowerCase(),
        })
      }}
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
      default: "theme-gradient-btn",
    },
    routeName: {
      type: String,
      required: false,
    },
    search: {
      type: String,
      required: false,
    },
    minHeight: {
      type: String,
      required: false,
      default: "flex grow",
    },
  },
};
</script>
