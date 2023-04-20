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
import { defineRule } from "vee-validate";

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
      textTheme: "theme-blue",
      userLang: "sq",
      sidebar: true,
    };
  },
  created() {
    defineRule("required", (value) => {
      if (!value || typeof value !== "number" ? !value?.length : false) {
        return this.$t("isRequired");
      }
      return true;
    });

    defineRule("minMax", (value, [min, max]) => {
      if (!value || !value.length) {
        return true;
      }
      const numericValue = Number(value);
      if (numericValue < min) {
        return this.$t("minValue", { min });
      }
      if (numericValue > max) {
        return this.$t("maxValue", { max });
      }
      return true;
    });
    this.$store.dispatch("userModule/getCurrentUser").catch(() => {
      logoutUser();
      this.$router.push({ name: "signin" });
    });
    const initUserTheme =
      this.getTheme("theme-preference") || this.getMediaPreference();
    const initTextTheme = this.getTheme("text-theme") || this.textTheme;
    this.setTheme(initUserTheme);
    this.setTextTheme(initTextTheme);
    const initUserLang = this.getLang();
    this.setLang(initUserLang || "sq");
    this.setUserData();
    // this.$tours["dashboardTour"].start();
  },
  methods: {
    setTheme(theme) {
      localStorage.setItem("theme-preference", theme);
      this.userTheme = theme;
      document.documentElement.className = theme;
    },
    setTextTheme(theme) {
      localStorage.setItem("text-theme", theme);
      this.textTheme = theme;
      document.body.className = theme;
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
    getTheme(theme) {
      return localStorage.getItem(theme);
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
