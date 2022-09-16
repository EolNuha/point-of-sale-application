<template>
  <NavBar />
  <SideBar />
  <router-view class="router-view" />
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";

export default {
  components: {
    NavBar,
    SideBar,
  },
  watch: {
    $route: {
      immediate: true,
      handler(to) {
        document.title = to.meta.title || "Desktop App";
      },
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.router-view {
  margin-left: 16rem;
}
.min-h-screen {
  min-height: calc(100vh - 60px) !important;
}
</style>
