<template>
  <template v-if="iconType === 'outline'">
    <outline-hero-icons :iconName="iconName" :iconClass="iconClass" />
  </template>
  <template v-if="iconType === 'solid' && iconSize === '24'">
    <solid-hero-icons :iconName="iconName" :iconClass="iconClass" />
  </template>
  <template v-if="iconType === 'solid' && iconSize === '20'">
    <solid-hero-icons-20 :iconName="iconName" :iconClass="iconClass" />
  </template>
  <template v-if="iconType === 'custom'">
    <custom-icons :iconName="iconName" :iconClass="iconClass" />
  </template>
</template>

<script>
import OutlineHeroIcons from "./OutlineIcon24.vue";
import SolidHeroIcons from "./SolidIcon24.vue";
import SolidHeroIcons20 from "./SolidIcon20.vue";
import CustomIcons from "./CustomIcons.vue";

export default {
  components: {
    OutlineHeroIcons,
    SolidHeroIcons,
    SolidHeroIcons20,
    CustomIcons,
  },
  props: {
    iconType: { type: String, required: false, default: "outline" },
    iconSize: { type: String, required: false, default: "24" },
    iconName: { type: String, required: true },
    iconClass: { type: String, required: false, default: "w-5 h-5" },
  },
};
</script>
