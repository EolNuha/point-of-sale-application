<template>
  <NavBar v-if="!$route.meta.hideNavbar" />
  <SideBar />
  <router-view class="router-view" id="main"></router-view>
  <!-- v-slot="{ Component }" -->
  <!-- <transition name="fade" mode="out-in">
      <component :is="Component" :key="$route.path" />
    </transition> -->
  <!-- <v-tour
    name="dashboardTour"
    :steps="steps"
    :callbacks="myCallbacks"
    :options="{ highlight: true, backdrop: true }"
  ></v-tour> -->
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";
import { logoutUser } from "@/router/auth/index";
import moment from "moment";
import "moment/locale/es";

export default {
  components: {
    NavBar,
    SideBar,
  },
  watch: {
    $route: {
      handler(to) {
        document.title = this.$t(to.meta.title) || "Desktop App";
      },
    },
  },
  data() {
    return {
      userTheme: "light",
      userLang: "en",
    };
  },
  created() {
    this.$store.dispatch("userModule/getCurrentUser").catch(() => {
      logoutUser();
      this.$router.push({ name: "signin" });
    });
    this.$store.dispatch("notificationsModule/checkProductExpiration");
  },
  mounted() {
    const initUserTheme = this.getTheme() || this.getMediaPreference();
    this.setTheme(initUserTheme);
    const initUserLang = this.getLang();
    this.setLang(initUserLang || "en");
    // this.$tours["dashboardTour"].start();
  },
  methods: {
    setTheme(theme) {
      localStorage.setItem("theme-preference", theme);
      this.userTheme = theme;
      document.documentElement.className = theme;
    },
    toggleTheme() {
      const activeTheme = localStorage.getItem("theme-preference");
      if (activeTheme === "light") {
        this.setTheme("dark");
      } else {
        this.setTheme("light");
      }
    },
    getMediaPreference() {
      const hasDarkPreference = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
      if (hasDarkPreference) {
        return "dark";
      } else {
        return "light";
      }
    },
    getTheme() {
      return localStorage.getItem("theme-preference");
    },
    getLang() {
      return localStorage.getItem("lang");
    },
    setLang(lang) {
      localStorage.setItem("lang", lang);
      this.$i18n.locale = lang;
      this.userLang = lang;
      moment.locale(lang);
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/index.scss";
</style>
