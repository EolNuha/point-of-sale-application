<template>
  <div class="main-div">
    <div
      class="text-blue-500 text-green-500 text-red-500 text-purple-500 text-orange-500 text-yellow-500"
    ></div>
    <h5
      class="text-3xl font-bold leading-none text-gray-900 dark:text-white mb-5"
    >
      {{ $t("theme") }}
    </h5>
    <div class="w-full bg-transparent rounded">
      <div>
        <ul role="list" class="flex flex-col gap-2">
          <li
            class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white cursor-pointer"
            @click="
              () => {
                $root.setTheme('light');
              }
            "
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <IconC iconName="SunIcon" iconClass="w-8 h-8" />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-lg font-medium text-gray-900 truncate dark:text-white"
                >
                  {{ $t("lightTheme") }}
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {{ $t("changeToTheme") }}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <input
                  type="radio"
                  :checked="$root.userTheme === 'light'"
                  class="dark:bg-neutral-700 text-theme-500"
                />
              </div>
            </div>
          </li>
          <li
            class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white cursor-pointer"
            @click="
              () => {
                $root.setTheme('dark');
              }
            "
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <IconC iconName="MoonIcon" iconClass="w-8 h-8" />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-lg font-medium text-gray-900 truncate dark:text-white"
                >
                  {{ $t("darkTheme") }}
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {{ $t("changeToTheme") }}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <input
                  type="radio"
                  :checked="$root.userTheme === 'dark'"
                  class="dark:bg-neutral-700 text-theme-500"
                />
              </div>
            </div>
          </li>
          <h5
            class="text-3xl font-bold leading-none text-gray-900 dark:text-white my-4"
          >
            {{ $t("colors") }}
          </h5>
          <template
            v-for="item in [
              'blue',
              'red',
              'purple',
              'green',
              'orange',
              'yellow',
            ]"
            :key="item"
          >
            <li
              class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white cursor-pointer"
              @click="
                () => {
                  $root.setTextTheme(`theme-${item}`);
                }
              "
            >
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <IconC
                    :key="item"
                    iconType="custom"
                    iconName="DropletIcon"
                    :iconClass="`w-8 h-8 text-${item}-500`"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <p
                    class="text-lg font-medium text-gray-900 truncate dark:text-white"
                  >
                    {{ $t(item) }}
                  </p>
                  <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                    {{ $t("changeToColor") }}
                  </p>
                </div>
                <div
                  class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
                >
                  <input
                    type="radio"
                    :checked="$root.textTheme === `theme-${item}`"
                    :class="`dark:bg-neutral-700 text-theme-500`"
                  />
                </div>
              </div>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
export default {};
</script>
