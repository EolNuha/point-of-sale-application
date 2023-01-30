<template>
  <li v-if="item.children">
    <button
      type="button"
      class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded transition duration-75 group hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-600"
      @click="() => (isOpened = !isOpened)"
    >
      <IconC
        iconType="outline"
        :iconName="item.icon"
        :iconClass="
          isOpened
            ? 'flex-shrink-0 w-6 h-6 text-black transition duration-75 group-hover:text-gray-900 dark:text-white dark:group-hover:text-white'
            : 'flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white'
        "
      />
      <span
        class="flex-1 ml-3 text-left whitespace-nowrap"
        :class="
          isOpened ? 'font-medium text-black dark:text-white' : 'font-normal'
        "
        sidebar-toggle-item=""
        >{{ $t(item.title) }}</span
      >
      <IconC
        iconName="ChevronRightIcon"
        :iconClass="
          isOpened
            ? 'w-4 h-4 transform rotate-90 transition duration-200 ease-in-out text-theme-500'
            : 'w-4 h-4 transition duration-200 ease-in-out'
        "
      />
    </button>
    <ul :id="item.title" class="py-2 space-y-2" :class="{ hidden: !isOpened }">
      <template v-for="child in item.children" :key="child.route">
        <li v-if="$can(child.action, child.subject)">
          <router-link
            :to="{ name: child.route }"
            class="flex items-center p-2 pl-11 w-full text-base font-normal text-gray-900 rounded transition duration-75 group hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-600"
            >{{ $t(child.title) }}</router-link
          >
        </li>
      </template>
    </ul>
  </li>
  <li v-else>
    <router-link
      :to="{ name: item.route }"
      class="flex items-center p-2 w-full text-base font-normal text-gray-900 rounded transition duration-75 group hover:bg-neutral-100 dark:text-white dark:hover:bg-neutral-600"
    >
      <IconC
        iconType="outline"
        :iconName="item.icon"
        iconClass="flex-shrink-0 w-6 h-6 text-gray-500 transition duration-75 group-hover:text-gray-900 dark:text-gray-400 dark:group-hover:text-white"
      />
      <span class="ml-3">{{ $t(item.title) }}</span>
    </router-link>
  </li>
</template>

<script>
export default {
  props: {
    item: null,
  },
  data() {
    return {
      isOpened: false,
    };
  },
};
</script>
