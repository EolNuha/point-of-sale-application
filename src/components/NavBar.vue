<template>
  <nav
    class="bg-white dark:bg-gray-900 shadow-md dark:shadow-gray-700 border-gray-200 px-2 sm:px-4 py-3 sticky top-0 left-0 right-0"
  >
    <div class="flex flex-wrap items-center justify-between">
      <div class="inline-flex items-center">
        <button
          class="hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-xl mr-3 p-1"
          @click="closeSide"
          v-show="sideBar"
        >
          <IconC
            iconName="XMarkIcon"
            iconClass="w-6 h-6 text-gray-700 dark:text-gray-300"
          />
        </button>
        <button
          class="hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-xl mr-3 p-1"
          @click="openSide"
          v-show="!sideBar"
        >
          <IconC
            iconName="Bars3CenterLeftIcon"
            iconClass="w-6 h-6 text-gray-700 dark:text-gray-300"
          />
        </button>
        <router-link
          :to="{ name: 'home' }"
          class="flex items-center w-auto sm:w-[14rem]"
        >
          <img
            src="https://flowbite.com/docs/images/logo.svg"
            class="mr-3 h-6 sm:h-9"
            alt="Logo"
          />
          <div>
            <span
              class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
            >
              Egzoni
            </span>
            <span
              class="text-sm font-semibold whitespace-nowrap dark:text-gray-300"
            >
              Market
            </span>
          </div>
        </router-link>
      </div>
      <ol class="hidden sm:inline-flex mr-auto space-x-1 md:space-x-3">
        <li class="inline-flex items-center">
          <router-link
            :to="{ name: 'home' }"
            class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          >
            <IconC iconName="HomeIcon" iconClass="w-4 h-4 mr-2" />
            Dashboard
          </router-link>
        </li>
        <li v-for="item in $route.meta.breadcrumb" :key="item">
          <div class="flex items-center">
            <IconC
              iconSize="20"
              iconType="solid"
              iconName="ChevronRightIcon"
              iconClass="w-6 h-6 text-gray-400"
            />
            <router-link
              :to="{ name: item.to, query: item.query ? $route.query : {} }"
              class="ml-1 text-sm font-medium text-gray-700 hover:text-gray-900 md:ml-2 dark:text-gray-400 dark:hover:text-white"
              :class="item.active ? '!text-blue-600' : ''"
              >{{ item.text($route) }}</router-link
            >
          </div>
        </li>
      </ol>
      <button
        id="dropdownUserAvatarButton"
        @click="
          $toggleDropdown({
            targetEl: `dropdownUserAvatarMenu`,
            triggerEl: `dropdownUserAvatarButton`,
          })
        "
        class="inline-flex items-center mx-3 text-sm font-medium text-gray-900 dark:text-white gap-1 mr-2 capitalize"
        type="button"
      >
        {{ user.firstName }} {{ user.lastName }}
        <span class="sr-only">Open user menu</span>
        <img
          class="w-7 h-7 rounded-full"
          src="https://flowbite.com/docs/images/people/profile-picture-3.jpg"
          alt="user photo"
        />
      </button>
      <div
        id="dropdownUserAvatarMenu"
        class="hidden z-10 w-44 bg-white rounded divide-y divide-gray-100 shadow-md dark:shadow-gray-600 dark:bg-gray-900 dark:divide-gray-600"
        style="inset: 0px auto auto -10px !important"
      >
        <div class="py-3 px-4 text-sm text-gray-900 dark:text-white">
          <div>{{ user.firstName }} {{ user.lastName }}</div>
          <div class="font-medium truncate text-gray-500 dark:text-gray-300">
            @{{ user.username }}
          </div>
        </div>
        <ul
          class="py-1 text-sm text-gray-500 dark:text-gray-200"
          aria-labelledby="dropdownUserAvatarButton"
        >
          <li>
            <router-link
              :to="{ name: 'home' }"
              class="inline-flex items-center font-normal gap-1 w-full text-sm py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <IconC iconName="Cog6ToothIcon" iconClass="w-5 h-5" />
              Settings</router-link
            >
          </li>
          <li>
            <button
              @click="toggleTheme"
              id="theme-toggle"
              type="button"
              class="inline-flex items-center w-full gap-1 py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <template v-if="!isDarkMode">
                <IconC iconName="MoonIcon" iconClass="w-5 h-5" />
                Dark Mode
              </template>
              <template v-if="isDarkMode">
                <IconC iconName="SunIcon" iconClass="w-5 h-5" />
                Light Mode
              </template>
            </button>
          </li>
        </ul>
        <div class="py-1">
          <button
            @click="logout"
            class="flex items-center w-full gap-1 py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
          >
            <IconC iconName="ArrowRightOnRectangleIcon" iconClass="h-5 w-5" />
            Sign out
          </button>
        </div>
      </div>
      <!-- <button
        data-collapse-toggle="navbar-default"
        type="button"
        class="inline-flex items-center p-1 ml-3 text-sm text-gray-500 rounded-xl md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700/50 dark:focus:ring-gray-600"
        aria-controls="navbar-default"
        aria-expanded="false"
      >
        <span class="sr-only">Open main menu</span>
        <IconC iconName="Bars3Icon" iconClass="w-6 h-6" />
      </button> -->
      <!-- <div class="hidden w-full md:block md:w-auto" id="navbar-default">
        <ul
          class="flex flex-col items-center p-4 mt-4 bg-gray-50 rounded-lg border border-gray-100 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"
        >
          <li></li>
          <li>
            <button
              @click="toggleTheme"
              id="theme-toggle"
              type="button"
              class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm"
            >
              <IconC
                iconName="MoonIcon"
                iconClass="w-5 h-5"
                v-if="!isDarkMode"
              />
              <IconC iconName="SunIcon" iconClass="w-5 h-5" v-if="isDarkMode" />
            </button>
          </li>
        </ul>
      </div> -->
    </div>
  </nav>
</template>

<script>
import { logoutUser } from "@/router/auth/index";
export default {
  name: "NavBar",
  data() {
    return {
      sideBar: true,
      isDarkMode:
        localStorage.getItem("theme-preference") === "dark" ? true : false,
    };
  },
  created() {
    this.closeSide();
    this.openSide();
  },
  mounted() {
    this.$store.dispatch("userModule/getCurrentUser");
  },
  computed: {
    user() {
      return this.$store.state.userModule.currentUser;
    },
  },
  methods: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      this.$parent.toggleTheme();
    },
    closeSide() {
      document.getElementById("app").classList.remove("sidebar-opened");
      this.sideBar = false;
    },
    openSide() {
      document.getElementById("app").classList.add("sidebar-opened");
      this.sideBar = true;
    },
    logout() {
      logoutUser("signin");
      this.$toast.success("You have successfully signed out!");
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_navbar.scss";
</style>
