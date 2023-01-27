<template>
  <button
    id="dropdownNotificationButton"
    class="inline-flex items-center text-sm font-medium text-center text-gray-500 hover:text-gray-900 focus:outline-none dark:hover:text-white dark:text-gray-400 w-9 ml-auto"
    type="button"
    @click="
      $toggleDropdown({
        targetEl: `dropdownNotification`,
        triggerEl: `dropdownNotificationButton`,
      });
      getNotifications();
    "
  >
    <IconC iconName="BellIcon" iconType="solid" iconClass="w-6 h-6" />
    <div class="flex relative" v-if="hasUnread">
      <div
        class="inline-flex relative -top-2 right-3 w-3 h-3 bg-red-500 rounded-full border-2 border-white dark:border-gray-900"
      ></div>
    </div>
  </button>
  <!-- Dropdown menu -->
  <div
    id="dropdownNotification"
    class="hidden z-20 w-full max-w-xs bg-white divide-y divide-gray-100 shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800 dark:divide-gray-700 rounded"
    aria-labelledby="dropdownNotificationButton"
    data-popper-reference-hidden=""
    data-popper-escaped=""
    data-popper-placement="bottom"
    style="
      position: absolute;
      inset: 0px auto auto 0px;
      margin: 0px;
      transform: translate3d(0px, 2104px, 0px);
    "
  >
    <div
      class="block py-2 px-4 font-medium text-center text-gray-700 bg-neutral-50 dark:bg-neutral-800 dark:text-white rounded-t-md"
    >
      {{ $t("notifications") }}
    </div>
    <div class="divide-y divide-gray-200 dark:divide-gray-700">
      <div v-if="isLoading" class="flex justify-center items-center py-5">
        <IconC
          iconType="custom"
          iconName="SpinnerIcon"
          iconClass="w-6 h-6 text-gray-200 animate-spin fill-theme-600"
        />
      </div>
      <router-link
        v-else
        class="flex py-3 px-4"
        :class="
          !item.read
            ? 'bg-neutral-200/50 hover:bg-neutral-200/75 dark:bg-neutral-900/50 dark:hover:bg-neutral-900/75 border-l-[3px] !border-l-theme-500'
            : 'hover:bg-neutral-100 dark:hover:bg-neutral-700/50'
        "
        v-for="item in notifications"
        :key="item.id"
        :to="{
          name: 'product-view',
          params: { productId: item.toId },
          query: { notificationId: item.id },
        }"
      >
        <div class="pl-3 w-full">
          <div class="text-gray-500 text-sm mb-1.5 dark:text-gray-400">
            {{ localizedMessage(item.message) }}
          </div>
          <div class="text-xs text-theme-600 dark:text-theme-500">
            {{ dateSince(item.dateCreated) }}
          </div>
        </div>
      </router-link>
    </div>
    <router-link
      :to="{ name: 'notifications' }"
      class="rounded-b-md block py-2 text-sm font-medium text-center text-gray-900 bg-neutral-50 hover:bg-neutral-100 dark:bg-neutral-800 dark:hover:bg-neutral-700 dark:text-white"
    >
      <div class="inline-flex items-center">
        <IconC
          iconName="EyeIcon"
          iconType="solid"
          iconClass="mr-2 w-4 h-4 text-gray-500 dark:text-gray-400"
        />
        {{ $t("viewAll") }}
      </div>
    </router-link>
  </div>
</template>
<script>
import moment from "moment";
export default {
  data() {
    return {
      isLoading: false,
      isDropdownOpened: false,
    };
  },
  computed: {
    notifications() {
      return this.$store.state.notificationsModule.notifications.data || [];
    },
    hasUnread() {
      return !!this.notifications.find((x) => x.read === false);
    },
    dateSince() {
      return (date) => moment(date).fromNow();
    },
  },
  methods: {
    localizedMessage(message) {
      return message
        .replace("expires in", this.$t("expiresIn"))
        .replace("days", this.$t("days"))
        .replace("Product", this.$t("product"))
        .replace("has expired", this.$t("hasExpired"));
    },
    async getNotifications() {
      if (!this.isDropdownOpened) {
        this.isLoading = true;
        await this.$store
          .dispatch("notificationsModule/getNotifications")
          .then(() => {
            this.isLoading = false;
          });
      }
      this.isDropdownOpened = !this.isDropdownOpened;
    },
  },
};
</script>
