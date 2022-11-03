<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="overflow-hidden rounded-xl mb-5 min-h-[80vh] relative">
      <!-- {{ hasStarredMessages }} -->
      <div
        class="overflow-x-auto overflow-y-hidden scrollbar-style text-gray-500 dark:text-gray-400"
      >
        <div
          class="border-l-[3px] border-l-white dark:border-gray-700 bg-white rounded-t dark:bg-gray-900 py-0 border-b flex flex-row"
        >
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
              class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
            >
              <input
                type="checkbox"
                class="rounded cursor-pointer text-blue-600 border-gray-500 focus:ring-0 dark:bg-gray-700 dark:border-gray-600"
                :checked="areAllSelected"
              />
              <div
                :id="`select-all-tooltip`"
                role="tooltip"
                class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
              >
                {{ $t("selectAll") }}
              </div>
            </button>
          </div>
          <template v-if="selectedItems.length !== 0">
            <div class="px-1">
              <button
                id="star-all-tooltip-btn"
                @click="toggleStarStatus()"
                class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
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
                  class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                >
                  {{ hasStarredMessages ? $t("removeStar") : $t("addStar") }}
                </div>
              </button>
            </div>
            <div class="px-3">
              <button
                id="read-all-tooltip-btn"
                @click="toggleReadStatus()"
                class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
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
                  class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                >
                  {{ hasUnreadMessages ? $t("markRead") : $t("markUnread") }}
                </div>
              </button>
            </div>
          </template>
        </div>
        <div
          class="border-l-[3px] border-l-white bg-white dark:bg-gray-900 py-0 border-b dark:border-gray-700 px-2"
        >
          <ul
            class="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 dark:text-gray-400"
          >
            <li
              class="mr-2"
              @click="() => ((activeTab = 'all'), (colName = null))"
            >
              <p
                :class="
                  activeTab === 'all'
                    ? 'inline-flex items-center cursor-pointer p-4 text-blue-600 rounded-t-lg border-b-4 border-blue-600 active dark:text-blue-500 dark:border-blue-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC iconName="InboxIcon" iconClass="w-6 h-6 mr-2" />All
                Notifications
              </p>
            </li>
            <li
              class="mr-2"
              @click="() => ((activeTab = 'star'), (colName = 'star'))"
            >
              <p
                :class="
                  activeTab === 'star'
                    ? 'inline-flex items-center cursor-pointer p-4 text-blue-600 rounded-t-lg border-b-4 border-blue-600 active dark:text-blue-500 dark:border-blue-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC
                  iconType="outline"
                  iconName="StarIcon"
                  iconClass="w-6 h-6 mr-2"
                />Starred
              </p>
            </li>
            <li
              class="mr-2"
              @click="() => ((activeTab = 'unread'), (colName = 'read'))"
            >
              <p
                :class="
                  activeTab === 'unread'
                    ? 'inline-flex items-center cursor-pointer p-4 text-blue-600 rounded-t-lg border-b-4 border-blue-600 active dark:text-blue-500 dark:border-blue-500 group'
                    : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
                "
              >
                <IconC
                  iconType="outline"
                  iconName="EnvelopeIcon"
                  iconClass="w-6 h-6 mr-2"
                />Unread
              </p>
            </li>
          </ul>
        </div>
        <table class="w-full text-sm text-left relative">
          <OverlayC v-if="isTableLoading" :minHeight="`min-h-65`" />
          <div
            class="w-full z-50 overflow-hidden flex flex-col items-center justify-center min-h-65"
            v-if="notifications.length === 0 && !isTableLoading"
          >
            <IconC iconName="NoSymbolIcon" iconClass="w-12 h-12" />
            <h2 class="text-gray-700 dark:text-gray-300 text-2xl my-4">
              {{ `No notifications have been added yet...` }}
            </h2>
          </div>
          <tbody>
            <template v-for="item in notifications" :key="item.id">
              <tr
                class="border-l-[3px] border-l-white hover:border-l-gray-200 bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:shadow-[inset_0_0px_15px_-2px_rgba(0,0,0,0.2)] hover:dark:shadow-[inset_0_0px_15px_-2px_rgba(255,255,255,0.2)] cursor-pointer"
                :class="{
                  '!border-l-blue-500': !item.read,
                  'bg-gray-100 dark:bg-gray-700  border-l-gray-100':
                    selectedItems.some((obj) => obj?.id === item.id),
                }"
                @click="
                  $router.push({
                    name: 'product-view',
                    params: { productId: item.toId },
                    query: { notificationId: item.id },
                  })
                "
              >
                <td class="py-2 px-3 w-1.5">
                  <button
                    :id="`select-${item.id}-tooltip-btn`"
                    @click.stop
                    @click="toggleSelectNotification(item)"
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                    @mouseover="
                      $showTooltip({
                        targetEl: `select-${item.id}-tooltip`,
                        triggerEl: `select-${item.id}-tooltip-btn`,
                      })
                    "
                  >
                    <input
                      type="checkbox"
                      class="rounded cursor-pointer text-blue-600 border-gray-500 focus:ring-0 dark:bg-gray-700 dark:border-gray-600"
                      :checked="
                        selectedItems.some((obj) => obj?.id === item.id)
                      "
                    />
                    <div
                      :id="`select-${item.id}-tooltip`"
                      role="tooltip"
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                      {{ $t("select") }}
                    </div>
                  </button>
                </td>
                <td class="py-2 px-1 w-1.5">
                  <button
                    :id="`star-${item.id}-tooltip-btn`"
                    @click.stop
                    @click="
                      toggleSingleNotification(item.id, item.read, !item.star)
                    "
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                    @mouseover="
                      $showTooltip({
                        targetEl: `star-${item.id}-tooltip`,
                        triggerEl: `star-${item.id}-tooltip-btn`,
                      })
                    "
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
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
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
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                    @mouseover="
                      $showTooltip({
                        targetEl: `read-${item.id}-tooltip`,
                        triggerEl: `read-${item.id}-tooltip-btn`,
                      })
                    "
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
                      class="inline-block absolute invisible z-10 p-1.5 text-sm text-white bg-gray-700 rounded-lg shadow-sm opacity-0 transition-opacity duration-300 tooltip"
                    >
                      {{ !item.read ? $t("markRead") : $t("markUnread") }}
                    </div>
                  </button>
                </td>
                <td class="py-2 px-3">
                  <div class="pl-3 w-full">
                    <div
                      class="text-gray-700 text-lg dark:text-gray-300"
                      :class="{ 'font-bold': !item.read }"
                    >
                      {{ localizedMessage(item.message) }}
                    </div>
                  </div>
                </td>
                <td class="py-2 px-6 w-48">
                  <div
                    class="text-sm text-right"
                    :class="{ 'font-bold': !item.read }"
                  >
                    {{ dateSince(item.dateCreated) }}
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
    };
  },
  computed: {
    pagination() {
      return (
        this.$store.state.notificationsModule.notificationsList.pagination || []
      );
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
        JSON.stringify(selectedItemsCopy.sort((a, b) => (a.id > b.id ? 1 : -1)))
      );
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
    this.getNotifications(this.currentPage);
  },
  methods: {
    syncData() {
      this.selectedItems.forEach((item) => {
        this.notifications.find((x) => x.id === item.id).read = item.read;
        this.notifications.find((x) => x.id === item.id).star = item.star;
      });
    },
    getNotifications(page) {
      this.$store
        .dispatch("notificationsModule/getNotificationsList", {
          per_page: 10,
          page: page,
          col_name: this.colName,
        })
        .then(() => {
          this.notifications =
            this.$store.state.notificationsModule.notificationsList.data;
          this.currentPage = page;
          this.isTableLoading = false;
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
          this.getNotifications(this.currentPage);
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
          this.getNotifications(this.currentPage);
          this.$store.dispatch("notificationsModule/getNotifications");
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
