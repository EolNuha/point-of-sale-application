<template>
  <div class="main-div">
    <div class="border-b border-gray-200 dark:border-gray-500 mb-5">
      <ul
        class="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 dark:text-gray-400"
      >
        <li class="mr-2" @click="() => (activeTab = 'outline')">
          <p
            :class="
              activeTab === 'outline'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-600 rounded-t-lg border-b-2 border-theme-600 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC
              iconName="ArrowDownCircleIcon"
              iconClass="w-6 h-6 mr-2"
            />Outline
          </p>
        </li>
        <li class="mr-2" @click="() => (activeTab = 'solid')">
          <p
            :class="
              activeTab === 'solid'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-600 rounded-t-lg border-b-2 border-theme-600 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC
              iconType="solid"
              iconName="ArrowDownCircleIcon"
              iconClass="w-6 h-6 mr-2"
            />Solid
          </p>
        </li>
      </ul>
    </div>
    <div class="grid grid-cols-6 gap-4">
      <div
        class="overflow-x-hidden flex items-center justify-center flex-col bg-neutral-300 dark:bg-neutral-700 rounded p-2.5 text-gray-700 dark:text-gray-300 cursor-pointer"
        v-for="icon in icons"
        :key="icon"
        @click="copy(icon)"
      >
        <outline-hero-icons
          v-if="activeTab === 'outline'"
          :iconName="icon"
          iconClass="w-10 h-10 mb-3"
        />
        <solid-hero-icons
          v-if="activeTab === 'solid'"
          :iconName="icon"
          iconClass="w-10 h-10 mb-3"
        />
        {{ icon }}
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Icons from "@/components/icons/icons.json";
import OutlineHeroIcons from "@/components/icons/OutlineIcon24.vue";
import SolidHeroIcons from "@/components/icons/SolidIcon24.vue";
export default {
  components: { OutlineHeroIcons, SolidHeroIcons },
  data() {
    return {
      isLoading: false,
      activeTab: "outline",
      icons: Icons,
    };
  },
  methods: {
    async copy(text) {
      await navigator.clipboard.writeText(text);
      this.$toast.success("Icon name copied!");
    },
  },
};
</script>
