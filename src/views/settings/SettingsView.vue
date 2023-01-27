<template>
  <div class="main-div">
    <h5
      class="text-3xl font-bold leading-none text-gray-900 dark:text-white mb-5"
    >
      Settings
    </h5>
    <div class="w-full bg-transparent rounded">
      <div>
        <ul role="list" class="flex flex-col gap-2">
          <router-link
            :to="{ name: 'permissions' }"
            v-if="$can('read', 'permissions')"
          >
            <li
              class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white"
            >
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <IconC iconName="LockClosedIcon" iconClass="w-6 h-6" />
                </div>
                <div class="flex-1 min-w-0">
                  <p
                    class="text-lg font-medium text-gray-900 truncate dark:text-white"
                  >
                    {{ $t("permissions") }}
                  </p>
                  <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                    {{ $t("changeUserPermissions") }}
                  </p>
                </div>
                <div
                  class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
                >
                  <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4" />
                </div>
              </div>
            </li>
          </router-link>
          <router-link :to="{ name: 'languages' }">
            <li
              class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white"
            >
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <IconC iconName="LanguageIcon" iconClass="w-6 h-6" />
                </div>
                <div class="flex-1 min-w-0">
                  <p
                    class="text-lg font-medium text-gray-900 truncate dark:text-white"
                  >
                    {{ $t("languages") }}
                  </p>
                  <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                    {{ $t("changeLanguage") }}
                  </p>
                </div>
                <div
                  class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
                >
                  <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4" />
                </div>
              </div>
            </li>
          </router-link>
          <router-link :to="{ name: 'theme' }">
            <li
              class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white"
            >
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <IconC iconName="SunIcon" iconClass="w-6 h-6" />
                </div>
                <div class="flex-1 min-w-0">
                  <p
                    class="text-lg font-medium text-gray-900 truncate dark:text-white"
                  >
                    {{ $t("theme") }}
                  </p>
                  <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                    {{ $t("changeThemeColors") }}
                  </p>
                </div>
                <div
                  class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
                >
                  <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4" />
                </div>
              </div>
            </li>
          </router-link>
          <li
            class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white"
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <IconC iconName="InformationCircleIcon" iconClass="w-6 h-6" />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-lg font-medium text-gray-900 truncate dark:text-white"
                >
                  About
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  Information about the desktop software
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <IconC iconName="ChevronRightIcon" iconClass="w-4 h-4" />
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
export default {};
</script>
