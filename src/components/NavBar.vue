<template>
  <nav
    class="bg-white dark:bg-neutral-900 shadow-md dark:shadow-neutral-800 border-gray-200 px-2 sm:px-4 py-3 sticky top-0 left-0 right-0"
    id="navbar"
  >
    <div class="flex flex-wrap items-center justify-between">
      <div class="inline-flex items-center">
        <button
          class="p-1.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700 mr-3"
          @click="$root.closeSide"
          v-show="$root.sidebar"
        >
          <IconC
            iconName="XMarkIcon"
            iconClass="w-6 h-6 text-gray-700 dark:text-gray-300"
          />
        </button>
        <button
          class="p-1.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700 mr-3"
          @click="$root.openSide"
          v-show="!$root.sidebar"
        >
          <IconC
            iconName="Bars3CenterLeftIcon"
            iconClass="w-6 h-6 text-gray-700 dark:text-gray-300"
          />
        </button>
        <router-link
          :to="{ name: 'dashboard' }"
          class="flex items-center w-auto sm:w-[14rem]"
        >
          <IconC
            v-if="!isThemeChanged"
            iconType="custom"
            iconName="FlowbiteIcon"
            iconClass="w-9 h-9 mr-2"
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
            :to="{ name: 'dashboard' }"
            class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
          >
            <IconC iconName="HomeIcon" iconClass="w-4 h-4 mr-2" />
            {{ $t("dashboard") }}
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
              :class="item.active ? '!text-theme-600' : ''"
              >{{ crumb(item) }}</router-link
            >
          </div>
        </li>
      </ol>
      <NotificationComponent v-if="$can('read', 'notifications')" />
      <button
        id="dropdownUserAvatarButton"
        @click="
          $toggleDropdown({
            targetEl: `dropdownUserAvatarMenu`,
            triggerEl: `dropdownUserAvatarButton`,
            placement: `top`,
          })
        "
        class="inline-flex items-center justify-end mx-3 text-sm font-medium text-gray-500 hover:text-gray-700 dark:hover:text-white dark:text-gray-400 gap-1 mr-2 capitalize md:min-w-[100px]"
        type="button"
      >
        <span class="hidden sm:inline"
          >{{ user.firstName }} {{ user.lastName }}</span
        >
        <span class="sr-only">Open user menu</span>
        <IconC iconType="solid" iconName="UserCircleIcon" iconClass="w-7 h-7" />
      </button>
      <div
        id="dropdownUserAvatarMenu"
        class="hidden z-10 w-44 bg-white rounded divide-y divide-gray-100 shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800 dark:divide-gray-600"
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
              :to="{ name: 'user-details', params: { userId: user.id || '1' } }"
              class="inline-flex items-center font-normal gap-1 w-full text-sm py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <IconC iconName="UserIcon" iconClass="w-5 h-5" />
              {{ $t("profile") }}</router-link
            >
          </li>
          <li>
            <router-link
              :to="{ name: 'settings' }"
              class="inline-flex items-center font-normal gap-1 w-full text-sm py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <IconC iconName="Cog8ToothIcon" iconClass="w-5 h-5" />
              {{ $t("settings") }}</router-link
            >
          </li>
        </ul>
        <div class="py-1">
          <button
            @click="logout"
            class="flex items-center w-full gap-1 py-2 px-4 text-sm text-gray-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 dark:text-gray-200 dark:hover:text-white"
          >
            <IconC iconName="ArrowRightOnRectangleIcon" iconClass="h-5 w-5" />
            {{ $t("signout") }}
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { logoutUser } from "@/router/auth/index";
import NotificationComponent from "@/components/notifications/NotificationComponent.vue";
export default {
  name: "NavBar",
  components: {
    NotificationComponent,
  },
  data() {
    return {
      sideBar: true,
      isThemeChanged: false,
    };
  },
  watch: {
    "$root.textTheme": {
      async handler() {
        this.isThemeChanged = true;
        await setTimeout(() => {}, 200);
        this.isThemeChanged = false;
      },
    },
  },
  created() {
    this.$root.closeSide();
    this.$root.openSide();
  },
  computed: {
    user() {
      return this.$store.state.userModule.currentUser;
    },
    crumb() {
      return (item) => this.$t(item.text(this.$route));
    },
  },
  methods: {
    logout() {
      logoutUser("signin");
      this.$toast.success(this.$t("signoutSuccess"));
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_navbar.scss";
</style>
