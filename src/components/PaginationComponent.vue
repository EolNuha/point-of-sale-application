<template>
  <div class="flex justify-between items-center flex-wrap gap-4">
    <div class="text-gray-700 dark:text-gray-400">
      {{ $t("viewingPage") }}
      <span class="rounded font-semibold text-gray-900 dark:text-white p-1">{{
        currentPage
      }}</span>
      {{ $t("with") }}
      <span
        class="rounded font-semibold text-gray-900 dark:text-gray-300 p-1"
        >{{ pagination.items }}</span
      >
      {{ $t("itemsTotal") }}
      <span
        class="rounded font-semibold text-gray-900 dark:text-gray-300 p-1"
        >{{ pagination.total }}</span
      >
    </div>
    <div aria-label="Page navigation" v-if="!(pagination.pages <= 1)">
      <ul class="inline-flex items-center -space-x-px">
        <li>
          <button
            :disabled="!pagination.has_prev"
            @click="$emit('pageChange', pagination.prev_num)"
            class="block py-2 px-3 ml-0 text-gray-500 bg-transparent rounded dark:text-gray-400"
            :class="
              pagination.has_prev
                ? 'hover:text-gray-700 dark:hover:text-white'
                : ''
            "
          >
            <span class="sr-only">Previous</span>
            <IconC
              iconType="solid"
              iconSize="20"
              iconName="ChevronLeftIcon"
              iconClass="w-5 h-5"
            />
          </button>
        </li>
        <div v-if="pagination.page_range[0] !== 1">
          <button
            @click="$emit('pageChange', 1)"
            aria-current="page"
            class="py-2 px-3 text-gray-500 bg-transparent border border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-white"
          >
            1
          </button>
          <span class="px-1 text-gray-500 dark:text-gray-400">...</span>
        </div>
        <li
          v-for="page in pagination.page_range"
          :key="page"
          @click="$emit('pageChange', page)"
        >
          <a
            href="#"
            onclick="return false;"
            aria-current="page"
            :class="
              page === currentPage
                ? 'py-2 px-3 rounded text-theme-600 bg-transparent border border-theme-500 hover:text-theme-700'
                : 'py-2 px-3 text-gray-500 bg-transparent border border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-white'
            "
            >{{ page }}</a
          >
        </li>
        <div
          v-if="
            pagination.page_range[pagination.page_range.length - 1] !==
            pagination.pages
          "
        >
          <span class="px-1 text-gray-500 dark:text-gray-400">...</span>
          <button
            @click="$emit('pageChange', pagination.pages)"
            aria-current="page"
            class="py-2 px-3 text-gray-500 bg-transparent border border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-white"
          >
            {{ pagination.pages }}
          </button>
        </div>
        <li>
          <button
            :disabled="!pagination.has_next"
            @click="$emit('pageChange', pagination.next_num)"
            class="block py-2 px-3 ml-0 text-gray-500 bg-transparent rounded dark:text-gray-400"
            :class="
              pagination.has_next
                ? 'hover:text-gray-700 dark:hover:text-white'
                : ''
            "
          >
            <span class="sr-only">Next</span>
            <IconC
              iconType="solid"
              iconSize="20"
              iconName="ChevronRightIcon"
              iconClass="w-5 h-5"
            />
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pagination: {
      type: null,
      required: false,
      default: null,
    },
    currentPage: {
      type: Number,
      required: false,
      default: 1,
    },
  },
};
</script>
