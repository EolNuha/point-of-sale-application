<template>
  <component v-if="isLoaded" :is="heroIcons[iconName]" :class="iconClass" />
</template>

<script>
import * as heroIcons from "@heroicons/vue/24/solid";

export default {
  data() {
    return {
      isLoaded: false,
      heroIcons: heroIcons,
    };
  },
  props: {
    iconName: String,
    iconClass: String,
  },
  mounted() {
    this.isLoaded = true;
  },
};
</script>
