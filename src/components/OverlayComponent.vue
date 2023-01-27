<template>
  <div
    wire:loading
    :class="outerDiv + minHeight"
    class="absolute top-0 left-0 right-0 bottom-0 w-full z-50 overflow-hidden flex flex-col items-center justify-center"
  >
    <div :class="innerDiv" class="loader ease-linear mb-4"></div>
  </div>
</template>
<script>
export default {
  props: {
    outerDiv: {
      type: String,
      required: false,
      default: "opacity-75 bg-neutral-100 dark:bg-neutral-900 ",
    },
    innerDiv: {
      type: String,
      required: false,
      default:
        "rounded-full border-t-theme-700 dark:border-t-theme-700 border-gray-400 dark:border-gray-400 border-4 w-12 h-12 ",
    },
    minHeight: {
      type: String,
      required: false,
      default: "flex grow",
    },
  },
};
</script>
<style lang="scss">
@import "/src/styles/components/_overlay.scss";
</style>
