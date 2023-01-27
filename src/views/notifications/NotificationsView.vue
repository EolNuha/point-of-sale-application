<template>
  <div class="main-div">
    <div
      id="hide-notification"
      class="flex items-center p-4 mb-4 bg-red-100 rounded dark:bg-red-500 text-red-700 dark:text-white"
      role="alert"
      v-show="getNotificationPercentage >= 80"
    >
      <IconC
        iconName="ExclamationCircleIcon"
        iconClass="flex-shrink-0 w-5 h-5"
      />
      <span class="sr-only">Info</span>
      <div class="ml-3 text-sm font-medium">
        <b
          >{{
            getNotificationPercentage >= 100
              ? $t("outOfSpace")
              : $t("almostOutOfSpace")
          }}
          ({{ getNotificationPercentage }}%).</b
        >
        {{
          getNotificationPercentage >= 100
            ? $t("outOfSpaceText")
            : $t("almostOutOfSpaceText")
        }}
      </div>
      <button
        id="hide-notification-btn"
        type="button"
        class="ml-auto -mx-1.5 -my-1.5 bg-red-100 rounded-full focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex h-8 w-8 dark:bg-red-500 dark:hover:bg-red-600"
        @click="
          $hideAlert({
            triggerEl: 'hide-notification-btn',
            targetEl: 'hide-notification',
          })
        "
      >
        <span class="sr-only">Close</span>
        <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
      </button>
    </div>
    <div class="overflow-hidden rounded mb-5 min-h-[80vh] flex grow relative">
      <div
        class="overflow-x-auto overflow-y-hidden scrollbar-style flex flex-col grow text-gray-500 dark:text-gray-400"
      >
        <div
          v-if="$can('execute', 'notifications')"
          class="border-l-[3px] border-l-white dark:border-gray-700 bg-white rounded-t dark:bg-neutral-900 py-0 border-b flex items-center justify-between flex-row"
        >
          <div class="flex flex-row">
            <div class="px-3">
              <button
                id="select-all-tooltip-btn"
                @click="
                  () =>
                    areAllSelected
                      ? (selectedItems = [])
                      : (selectedItems = JSON.parse(
                          JSON.stringify(notifications)
                        ))
                "
                @mouseover="
                  $showTooltip({
                    targetEl: `select-all-tooltip`,
                    triggerEl: `select-all-tooltip-btn`,
                  })
                "
                class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
              >
                <input
                  type="checkbox"
                  class="rounded cursor-pointer text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
                  :checked="areAllSelected"
                  :indeterminate="selectedItems.length > 0 && !areAllSelected"
                />
                <div
                  :id="`select-all-tooltip`"
                  role="tooltip"
                  class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                >
                  {{ $t("selectAll") }}
                </div>
              </button>
            </div>
            <template v-if="selectedItems?.length !== 0">
              <div class="px-1">
                <button
                  id="star-all-tooltip-btn"
                  @click="toggleStarStatus()"
                  class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                  @mouseover="
                    $showTooltip({
                      targetEl: `star-all-tooltip`,
                      triggerEl: `star-all-tooltip-btn`,
                    })
                  "
                >
                  <IconC
                    v-if="hasStarredMessages"
                    iconName="StarIcon"
                    iconType="solid"
                    iconClass="w-5 h-5 text-yellow-300"
                  />
                  <IconC
                    v-else
                    iconName="StarIcon"
                    iconType="outline"
                    iconClass="w-5 h-5"
                  />
                  <div
                    :id="`star-all-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                  >
                    {{ hasStarredMessages ? $t("removeStar") : $t("addStar") }}
                  </div>
                </button>
              </div>
              <div class="px-3">
                <button
                  id="read-all-tooltip-btn"
                  @click="toggleReadStatus()"
                  class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                  @mouseover="
                    $showTooltip({
                      targetEl: `read-all-tooltip`,
                      triggerEl: `read-all-tooltip-btn`,
                    })
                  "
                >
                  <IconC
                    v-if="hasUnreadMessages"
                    iconName="EnvelopeOpenIcon"
                    iconType="outline"
                    iconClass="w-5 h-5"
                  />
                  <IconC
                    v-else
                    iconName="EnvelopeIcon"
                    iconType="outline"
                    iconClass="w-5 h-5"
                  />
                  <div
                    :id="`read-all-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                  >
                    {{ hasUnreadMessages ? $t("markRead") : $t("markUnread") }}
                  </div>
                </button>
              </div>
              <div class="px-1">
                <button
                  id="delete-all-tooltip-btn"
                  @click="deleteNotifications"
                  class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                  @mouseover="
                    $showTooltip({
                      targetEl: `delete-all-tooltip`,
                      triggerEl: `delete-all-tooltip-btn`,
                    })
                  "
                >
                  <IconC iconName="TrashIcon" iconClass="w-5 h-5" />
                  <div
                    :id="`delete-all-tooltip`"
                    role="tooltip"
                    class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                  >
                    {{ $t("delete") }}
                  </div>
                </button>
              </div>
            </template>
          </div>
          <div
            class="flex flex-col items-end gap-1 justify-center w-[150px] md:w-[250px] mx-3"
            v-if="total"
          >
            <div
              class="w-[150px] md:w-[200px] bg-neutral-300 rounded-full h-1.5 dark:bg-neutral-700"
            >
              <div
                class="h-1.5 rounded-full"
                :class="getStatus"
                :style="`width: ${getNotificationPercentage}%`"
              ></div>
            </div>
            <small class="text-gray-700 dark:text-gray-400"
              >{{ total }} {{ $t("of") }} {{ storage }} ({{
                getNotificationPercentage
              }}%) {{ $t("used") }}</small
            >
          </div>
        </div>
        <div
          class="border-l-[3px] border-l-white bg-white dark:bg-neutral-900 py-0 border-b dark:border-gray-700 px-2"
        >
          <ul
            class="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 dark:text-gray-400"
          >
            <li
              class="mr-2"
              @click="
                () => (
                  (activeTab = 'all'), (colName = null), (selectedItems = [])
                )
              "
            >
              <p
                :class="
                  activeTab === 'all'
                    ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC iconName="InboxIcon" iconClass="w-6 h-6 mr-2" />
                {{ $t("allNotifications") }}
              </p>
            </li>
            <li
              class="mr-2"
              @click="
                () => (
                  (activeTab = 'star'), (colName = 'star'), (selectedItems = [])
                )
              "
            >
              <p
                :class="
                  activeTab === 'star'
                    ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC
                  iconType="outline"
                  iconName="StarIcon"
                  iconClass="w-6 h-6 mr-2"
                />{{ $t("starred") }}
              </p>
            </li>
            <li
              class="mr-2"
              @click="
                () => (
                  (activeTab = 'unread'),
                  (colName = 'read'),
                  (selectedItems = [])
                )
              "
            >
              <p
                :class="
                  activeTab === 'unread'
                    ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC
                  iconType="outline"
                  iconName="EnvelopeIcon"
                  iconClass="w-6 h-6 mr-2"
                />{{ $t("unread") }}
              </p>
            </li>
          </ul>
        </div>
        <OverlayC v-if="isTableLoading" />
        <div
          class="w-full z-50 overflow-hidden flex flex-col items-center justify-center grow"
          v-if="notifications?.length === 0 && !isTableLoading"
        >
          <IconC iconName="NoSymbolIcon" iconClass="w-12 h-12" />
          <h2 class="text-gray-700 dark:text-gray-300 text-2xl my-4">
            {{ `No notifications have been added yet...` }}
          </h2>
        </div>
        <table class="w-full text-sm text-left">
          <tbody>
            <template v-for="item in notifications" :key="item.id">
              <tr
                class="group border-l-[3px] border-l-white hover:border-l-gray-200 bg-white hover:text-black hover:dark:text-white border-b dark:bg-neutral-900 dark:border-gray-700 hover:shadow-[inset_0_0px_15px_-2px_rgba(0,0,0,0.2)] hover:dark:shadow-[inset_0_0px_15px_-2px_rgba(255,255,255,0.2)] cursor-pointer"
                :class="{
                  '!border-l-theme-500': !item.read,
                  'bg-neutral-100 dark:bg-neutral-900/50  border-l-gray-100':
                    selectedItems.some((obj) => obj?.id === item.id),
                }"
                @click="
                  $can('read', 'products')
                    ? $router.push({
                        name: 'product-view',
                        params: { productId: item.toId },
                        query: { notificationId: item.id },
                      })
                    : ''
                "
              >
                <td
                  class="py-2 px-3 w-1.5"
                  v-if="$can('execute', 'notifications')"
                >
                  <button
                    :id="`select-${item.id}-tooltip-btn`"
                    @click.stop
                    @click="toggleSelectNotification(item)"
                    class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                    @mouseover="
                      $showTooltip({
                        targetEl: `select-${item.id}-tooltip`,
                        triggerEl: `select-${item.id}-tooltip-btn`,
                      })
                    "
                  >
                    <input
                      type="checkbox"
                      class="rounded cursor-pointer text-theme-600 border-gray-500 focus:ring-0 dark:bg-neutral-700 dark:border-gray-600"
                      :checked="
                        selectedItems.some((obj) => obj?.id === item.id)
                      "
                    />
                    <div
                      :id="`select-${item.id}-tooltip`"
                      role="tooltip"
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                      {{ $t("select") }}
                    </div>
                  </button>
                </td>
                <td
                  class="py-2 w-1.5"
                  :class="!$can('execute', 'notifications') ? 'px-3' : 'px-1'"
                >
                  <button
                    :id="`star-${item.id}-tooltip-btn`"
                    @click="
                      toggleSingleNotification(item.id, item.read, !item.star)
                    "
                    class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                    :class="
                      !$can('execute', 'notifications')
                        ? 'cursor-not-allowed'
                        : ''
                    "
                    @click.stop
                    @mouseover="
                      $showTooltip({
                        targetEl: `star-${item.id}-tooltip`,
                        triggerEl: `star-${item.id}-tooltip-btn`,
                      })
                    "
                    :disabled="!$can('execute', 'notifications')"
                  >
                    <IconC
                      v-if="!item.star"
                      iconName="StarIcon"
                      iconType="outline"
                      iconClass="w-5 h-5"
                    />
                    <IconC
                      v-else
                      iconName="StarIcon"
                      iconType="solid"
                      iconClass="w-5 h-5 text-yellow-300"
                    />
                    <div
                      :id="`star-${item.id}-tooltip`"
                      role="tooltip"
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                      {{ !item.star ? $t("addStar") : $t("removeStar") }}
                    </div>
                  </button>
                </td>
                <td class="py-2 px-3 w-1.5">
                  <button
                    :id="`read-${item.id}-tooltip-btn`"
                    @click.stop
                    @click="
                      toggleSingleNotification(item.id, !item.read, item.star)
                    "
                    class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50"
                    :class="
                      !$can('execute', 'notifications')
                        ? 'cursor-not-allowed'
                        : ''
                    "
                    @mouseover="
                      $showTooltip({
                        targetEl: `read-${item.id}-tooltip`,
                        triggerEl: `read-${item.id}-tooltip-btn`,
                      })
                    "
                    :disabled="!$can('execute', 'notifications')"
                  >
                    <IconC
                      v-if="!item.read"
                      iconName="EnvelopeOpenIcon"
                      iconType="outline"
                      iconClass="w-5 h-5"
                    />
                    <IconC
                      v-else
                      iconName="EnvelopeIcon"
                      iconType="outline"
                      iconClass="w-5 h-5"
                    />
                    <div
                      :id="`read-${item.id}-tooltip`"
                      role="tooltip"
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                      {{ !item.read ? $t("markRead") : $t("markUnread") }}
                    </div>
                  </button>
                </td>
                <td class="py-2 px-3">
                  <div class="pl-3 w-full">
                    <div
                      class="text-gray-700 text-lg dark:text-gray-400"
                      :class="{ 'font-bold': !item.read }"
                    >
                      {{ localizedMessage(item.message) }}
                    </div>
                  </div>
                </td>
                <td class="py-2 px-6 w-48">
                  <div
                    class="text-sm text-right flex items-center justify-end"
                    :class="{ 'font-bold': !item.read }"
                  >
                    <button
                      :id="`delete-${item.id}-tooltip-btn`"
                      @click.stop
                      @click="deleteNotification(item.id)"
                      class="p-3.5 rounded-full hover:bg-neutral-200/50 dark:hover:bg-neutral-800/50 hidden group-hover:block"
                      @mouseover="
                        $showTooltip({
                          targetEl: `delete-${item.id}-tooltip`,
                          triggerEl: `delete-${item.id}-tooltip-btn`,
                        })
                      "
                    >
                      <IconC iconName="TrashIcon" iconClass="w-5 h-5" />
                      <div
                        :id="`delete-${item.id}-tooltip`"
                        role="tooltip"
                        class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-neutral-700 rounded shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                      >
                        {{ $t("delete") }}
                      </div>
                    </button>
                    <span class="group-hover:hidden">{{
                      dateSince(item.dateCreated)
                    }}</span>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getNotifications($event)"
    />
  </div>
</template>
<script>
import moment from "moment";
export default {
  data() {
    return {
      notifications: [],
      selectedItems: [],
      isTableLoading: true,
      currentPage: 1,
      activeTab: "all",
      colName: null,
      total: null,
      storage: null,
    };
  },
  computed: {
    pagination() {
      return this.$store.getters[
        "notificationsModule/getNotificationsPagination"
      ];
    },
    dateSince() {
      return (date) => moment(date).calendar();
    },
    localizedMessage() {
      return (message) =>
        message
          .replace("expires in", this.$t("expiresIn"))
          .replace("days", this.$t("days"))
          .replace("Product", this.$t("product"))
          .replace("has expired", this.$t("hasExpired"));
    },
    hasUnreadMessages() {
      return !!this.selectedItems.find((x) => x.read === false);
    },
    hasStarredMessages() {
      return !!this.selectedItems.find((x) => x.star === true);
    },
    areAllSelected() {
      const notificationsCopy = JSON.parse(JSON.stringify(this.notifications));
      const selectedItemsCopy = JSON.parse(JSON.stringify(this.selectedItems));
      return (
        JSON.stringify(
          notificationsCopy.sort((a, b) => (a.id > b.id ? 1 : -1))
        ) ===
          JSON.stringify(
            selectedItemsCopy.sort((a, b) => (a.id > b.id ? 1 : -1))
          ) && this.notifications?.length !== 0
      );
    },
    getNotificationPercentage() {
      const percentage = Math.floor((this.total * 100) / this.storage) || 0;
      return percentage <= 100 ? percentage : 100;
    },
    getStatus() {
      const v = this.getNotificationPercentage;
      let color;
      if (v >= 80) {
        color = "bg-red-500";
      } else if (v < 80 && v > 50) {
        color = "bg-yellow-400";
      } else if (v <= 50) {
        color = "bg-theme-700";
      }
      return color;
    },
  },
  watch: {
    colName: {
      handler() {
        this.isTableLoading = true;
        this.getNotifications(1);
      },
    },
  },
  async created() {
    this.$store
      .dispatch("settingsModule/getSettingsType", {
        settingsType: "notification",
      })
      .then((response) => {
        this.storage = Number(response.data[0]?.settingsValue);
      });
    this.getNotifications(this.currentPage);
  },
  methods: {
    syncData() {
      this.selectedItems.forEach((item) => {
        this.notifications.find((x) => x.id === item.id).read = item.read;
        this.notifications.find((x) => x.id === item.id).star = item.star;
      });
    },
    async getNotifications(page, isLoading = true) {
      this.isTableLoading = isLoading;
      await this.$store
        .dispatch("notificationsModule/getNotificationsList", {
          per_page: 20,
          page: page,
          col_name: this.colName,
        })
        .then(() => {
          this.notifications =
            this.$store.getters["notificationsModule/getNotificationsList"];
          this.currentPage = page;
          this.isTableLoading = false;
          if (!this.colName) this.total = this.pagination.total;
        })
        .catch(() => {
          this.isTableLoading = false;
        });
    },
    toggleReadStatus() {
      this.selectedItems = this.selectedItems.map((el) => ({
        ...el,
        read: this.hasUnreadMessages,
      }));
      this.updateNotifications(this.selectedItems);
    },
    toggleStarStatus() {
      this.selectedItems = this.selectedItems.map((el) => ({
        ...el,
        star: !this.hasStarredMessages,
      }));
      this.updateNotifications(this.selectedItems);
    },
    updateNotifications(items) {
      this.syncData();
      this.$store
        .dispatch("notificationsModule/updateNotifications", {
          notifications: items,
        })
        .then(() => {
          this.getNotifications(this.currentPage, false);
          this.$store.dispatch("notificationsModule/getNotifications");
        });
    },
    toggleSingleNotification(notificationId, read, star) {
      const notification =
        this.notifications.find((x) => x.id === notificationId) || [];
      const selectedNotification =
        this.selectedItems.find((x) => x.id === notificationId) || [];

      notification.read = selectedNotification.read = read;
      notification.star = selectedNotification.star = star;

      this.$store
        .dispatch("notificationsModule/updateNotification", {
          id: notificationId,
          read: read,
          star: star,
        })
        .then(() => {
          this.getNotifications(this.currentPage, false);
          this.$store.dispatch("notificationsModule/getNotifications");
        });
    },
    deleteNotifications() {
      this.$store
        .dispatch("notificationsModule/deleteNotifications", {
          notifications: this.selectedItems,
        })
        .then(async () => {
          await this.getNotifications(this.currentPage, false);
          await this.$store.dispatch("notificationsModule/getNotifications");
          this.selectedItems = [];
          this.$toast.success(
            this.$t("deleteSuccess", { title: this.$t("notifications") })
          );
        })
        .catch(async () => {
          await this.getNotifications(this.currentPage);
          this.$toast.warning(this.$t("somethingWrong"));
        });
    },
    deleteNotification(id) {
      const notificationIdx =
        this.notifications.findIndex((x) => x.id === id) || null;
      this.notifications.splice(notificationIdx, 1);
      this.$store
        .dispatch("notificationsModule/deleteNotification", id)
        .then(async () => {
          await this.getNotifications(this.currentPage, false);
          await this.$store.dispatch("notificationsModule/getNotifications");
          this.$toast.success(
            this.$t("deleteSuccess", { title: this.$t("notification") })
          );
        })
        .catch(async () => {
          await this.getNotifications(this.currentPage);
          this.$toast.warning(this.$t("somethingWrong"));
        });
    },
    toggleSelectNotification(notification) {
      const idx = this.selectedItems.findIndex(
        (x) => x?.id === notification.id
      );
      if (idx !== -1) this.selectedItems.splice(idx, 1);
      if (idx === -1) this.selectedItems.push(notification);
    },
  },
};
</script>
<style lang="scss">
.shadow-inner-hover:hover {
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.5) !important;
}
</style>
