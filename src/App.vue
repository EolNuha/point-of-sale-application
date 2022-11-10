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
import UserData from "@/services/mixins/UserData";

export default {
  components: {
    NavBar,
    SideBar,
  },
  mixins: [UserData],
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
      sidebar: true,
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
    this.setUserData();
    // this.$tours["dashboardTour"].start();
  },
  methods: {
    setTheme(theme) {
      localStorage.setItem("theme-preference", theme);
      this.userTheme = theme;
      document.documentElement.className = theme;
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
    closeSide() {
      document.getElementById("app").classList.remove("sidebar-opened");
      this.sidebar = false;
    },
    openSide() {
      document.getElementById("app").classList.add("sidebar-opened");
      this.sidebar = true;
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/index.scss";
</style>
