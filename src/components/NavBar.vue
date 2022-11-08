<template>
  <nav
    class="bg-white dark:bg-gray-900 shadow-md dark:shadow-gray-700 border-gray-200 px-2 sm:px-4 py-3 sticky top-0 left-0 right-0"
    id="navbar"
  >
    <div class="flex flex-wrap items-center justify-between">
      <div class="inline-flex items-center">
        <button
          class="p-1.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50 mr-3"
          @click="closeSide"
          v-show="sideBar"
        >
          <IconC
            iconName="XMarkIcon"
            iconClass="w-6 h-6 text-gray-700 dark:text-gray-300"
          />
        </button>
        <button
          class="p-1.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50 mr-3"
          @click="openSide"
          v-show="!sideBar"
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
              :class="item.active ? '!text-blue-600' : ''"
              >{{ $t(item.text($route)) }}</router-link
            >
          </div>
        </li>
      </ol>
      <NotificationComponent v-if="$can('read', 'notification')" />
      <button
        id="dropdownUserAvatarButton"
        @click="
          $toggleDropdown({
            targetEl: `dropdownUserAvatarMenu`,
            triggerEl: `dropdownUserAvatarButton`,
            placement: `top`,
          })
        "
        class="inline-flex items-center justify-end mx-3 text-sm font-medium text-gray-900 dark:text-white gap-1 mr-2 capitalize md:min-w-[100px]"
        type="button"
      >
        <span class="hidden sm:inline"
          >{{ user.firstName }} {{ user.lastName }}</span
        >
        <span class="sr-only">Open user menu</span>
        <img
          class="w-7 h-7 rounded-full border-2 border-gray-500"
          src="http://localhost:5000/static/profile-2.png"
          alt="user photo"
        />
      </button>
      <div
        id="dropdownUserAvatarMenu"
        class="hidden z-10 w-44 bg-white rounded divide-y divide-gray-100 shadow-md shadow-gray-400/75 dark:shadow-gray-700/75 dark:bg-gray-800 dark:divide-gray-600"
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
              class="inline-flex items-center font-normal gap-1 w-full text-sm py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <IconC iconName="UserIcon" iconClass="w-5 h-5" />
              {{ $t("profile") }}</router-link
            >
          </li>
          <li>
            <button
              @click="toggleTheme"
              id="theme-toggle"
              type="button"
              class="inline-flex items-center w-full gap-1 py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white text-gray-500 dark:text-gray-400"
            >
              <template v-if="!isDarkMode">
                <IconC iconName="MoonIcon" iconClass="w-5 h-5" />
                {{ $t("darkMode") }}
              </template>
              <template v-if="isDarkMode">
                <IconC iconName="SunIcon" iconClass="w-5 h-5" />
                {{ $t("lightMode") }}
              </template>
            </button>
          </li>
          <li>
            <div class="flex items-center md:order-2">
              <button
                type="button"
                id="dropdownLangButton"
                @click="
                  $toggleDropdown({
                    targetEl: `dropdownLangMenu`,
                    triggerEl: `dropdownLangButton`,
                    placement: 'left',
                  })
                "
                data-dropdown-placement="left"
                class="flex items-center w-full gap-1 py-2 px-4 text-sm text-gray-500 rounded cursor-pointer hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                <template v-if="$i18n.locale === 'en'">
                  <IconC
                    iconType="custom"
                    iconName="EnglishFlagIcon"
                    iconClass="w-5 h-5 rounded-full"
                  />
                  English
                </template>
                <template v-if="$i18n.locale === 'sq'">
                  <IconC
                    iconType="custom"
                    iconName="AlbanianFlagIcon"
                    iconClass="w-5 h-5 rounded-full"
                  />
                  Shqip
                </template>
              </button>
              <!-- Dropdown -->
              <div
                class="hidden z-50 my-4 text-base list-none bg-white rounded divide-y divide-gray-100 shadow-md shadow-gray-400/75 dark:shadow-gray-700/75 dark:bg-gray-800 border dark:border-gray-600 dark:divide-gray-600"
                id="dropdownLangMenu"
                style="inset: 0px auto auto -50px !important"
              >
                <ul class="py-1 divide-y" role="none">
                  <li v-if="$i18n.locale !== 'en'">
                    <button
                      @click="
                        () => {
                          $parent.setLang('en'),
                            $toggleDropdown({
                              targetEl: `dropdownLangMenu`,
                              triggerEl: `dropdownLangButton`,
                            });
                        }
                      "
                      class="w-full py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
                      role="menuitem"
                    >
                      <div class="inline-flex items-center">
                        <IconC
                          iconType="custom"
                          iconName="EnglishFlagIcon"
                          iconClass="mr-2 w-5 h-5 rounded-full"
                        />
                        English
                      </div>
                    </button>
                  </li>
                  <li v-if="$i18n.locale !== 'sq'">
                    <button
                      @click="
                        () => {
                          $parent.setLang('sq'),
                            $toggleDropdown({
                              targetEl: `dropdownLangMenu`,
                              triggerEl: `dropdownLangButton`,
                            });
                        }
                      "
                      class="w-full py-2 px-4 text-sm text-gray-700 hover:bg-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
                      role="menuitem"
                    >
                      <div class="inline-flex items-center">
                        <IconC
                          iconType="custom"
                          iconName="AlbanianFlagIcon"
                          iconClass="mr-2 w-5 h-5 rounded-full"
                        />
                        Shqip
                      </div>
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </li>
        </ul>
        <div class="py-1">
          <button
            @click="logout"
            class="flex items-center w-full gap-1 py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-200 dark:hover:text-white"
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
      isDarkMode:
        localStorage.getItem("theme-preference") === "dark" ? true : false,
    };
  },
  created() {
    this.closeSide();
    this.openSide();
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
      this.$toast.success(this.$t("signoutSuccess"));
    },
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_navbar.scss";
</style>
