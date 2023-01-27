<template>
  <div class="main-div">
    <h5
      class="text-3xl font-bold leading-none text-gray-900 dark:text-white mb-5"
    >
      {{ $t("languages") }}
    </h5>
    <div class="w-full bg-transparent rounded">
      <div>
        <ul role="list" class="flex flex-col gap-2">
          <li
            class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white cursor-pointer"
            @click="
              () => {
                $root.setLang('en');
              }
            "
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <IconC
                  iconType="custom"
                  iconName="EnglishFlagIcon"
                  iconClass="w-8 h-8 rounded"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-lg font-medium text-gray-900 truncate dark:text-white"
                >
                  English
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {{ $t("changeToLanguage") }}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <input
                  type="radio"
                  :checked="$i18n.locale === 'en'"
                  class="dark:bg-neutral-700 text-theme-500"
                />
              </div>
            </div>
          </li>
          <li
            class="rounded px-4 sm:px-8 py-3 sm:py-4 bg-white dark:bg-neutral-900 hover:bg-neutral-100 hover:dark:bg-neutral-900/75 dark:text-white cursor-pointer"
            @click="
              () => {
                $root.setLang('sq');
              }
            "
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <IconC
                  iconType="custom"
                  iconName="AlbanianFlagIcon"
                  iconClass="w-8 h-8 rounded"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-lg font-medium text-gray-900 truncate dark:text-white"
                >
                  Shqip
                </p>
                <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                  {{ $t("changeToLanguage") }}
                </p>
              </div>
              <div
                class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
              >
                <input
                  type="radio"
                  :checked="$i18n.locale === 'sq'"
                  class="dark:bg-neutral-700 text-theme-500"
                />
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
