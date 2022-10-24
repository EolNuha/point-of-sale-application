<template>
  <NavBar v-if="!$route.meta.hideNavbar" />
  <SideBar />
  <router-view
    class="router-view duration-300"
    id="main"
    v-slot="{ Component }"
  >
    <transition name="fade" mode="out-in">
      <component :is="Component" :key="$route.path" />
    </transition>
  </router-view>
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
      // steps: [
      //   {
      //     target: "#dashboard-step-0",
      //     header: {
      //       title: "Get Started",
      //     },
      //     content: `Discover <strong>Vue Tour</strong>!`,
      //   },
      //   {
      //     target: "#dashboard-step-1",
      //     content: "An awesome plugin made with Vue.js!",
      //   },
      //   {
      //     target: "#dashboard-step-2",
      //     content:
      //       "Try it, you'll love it!<br>You can put HTML in the steps and completely customize the DOM to suit your needs.",
      //   },
      //   {
      //     target: "#navbar",
      //     content:
      //       "Try it, you'll love it!<br>You can put HTML in the steps and completely customize the DOM to suit your needs.",
      //   },
      //   {
      //     target: "#sidebar",
      //     content: "An awesome plugin made with Vue.js!",
      //     params: {
      //       placement: "right",
      //     },
      //   },
      // ],
    };
  },
  created() {
    this.$store.dispatch("userModule/getCurrentUser").catch(() => {
      logoutUser();
      this.$router.push({ name: "signin" });
    });
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
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/index.scss";
</style>
