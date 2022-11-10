<template>
  <div
    class="bg-white dark:bg-neutral-900 w-64 sidebar overflow-y-auto overflow-x-hidden duration-300 scrollbar-style shadow-md"
    id="sidebar"
    aria-label="Sidebar"
  >
    <div class="overflow-y-auto overflow-x-hidden py-4 px-3">
      <ul class="space-y-2">
        <template v-for="item in items" :key="item.title">
          <SidebarButton :item="item" v-if="$can(item.action, item.subject)" />
        </template>
      </ul>
    </div>
  </div>
</template>

<script>
import items from "@/navigation/sidebar";
import SidebarButton from "@/components/buttons/SidebarButton.vue";
export default {
  name: "SideBar",
  components: {
    SidebarButton,
  },
  setup() {
    return {
      items,
    };
  },
  computed: {
    user() {
      return this.$store.state.userModule.currentUser;
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_sidebar.scss";
</style>
