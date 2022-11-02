<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
    <div class="overflow-hidden rounded-xl mb-5 min-h-[80vh] relative">
      <!-- {{ areAllSelected }} -->
      <div
        class="overflow-x-auto overflow-y-hidden scrollbar-style text-gray-500 dark:text-gray-400"
      >
        <div
          class="border-l-[3px] border-l-white dark:border-gray-700 bg-white rounded-t dark:bg-gray-900 py-0 px-3 border-b flex flex-row"
        >
          <button
            @click.stop
            @click="
              () =>
                areAllSelected
                  ? (selectedItems = [])
                  : (selectedItems = notifications)
            "
            class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
          >
            <input
              type="checkbox"
              class="rounded cursor-pointer text-blue-600 border-gray-500 focus:ring-0 dark:bg-gray-700 dark:border-gray-600"
              :checked="areAllSelected"
            />
          </button>
          <template v-if="selectedItems.length !== 0">
            <button
              @click="toggleReadStatus()"
              class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
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
            </button>
          </template>
        </div>
        <table class="w-full text-sm text-left">
          <OverlayC v-if="isTableLoading" :minHeight="`min-h-[80vh]`" />
          <tbody>
            <template v-for="item in notifications" :key="item.id">
              <tr
                class="border-l-[3px] border-l-white bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:shadow-[inset_0_0px_15px_-2px_rgba(0,0,0,0.2)] hover:dark:shadow-[inset_0_0px_15px_-2px_rgba(255,255,255,0.2)] cursor-pointer"
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
                    @click.stop
                    @click="toggleSelectNotification(item)"
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                  >
                    <input
                      type="checkbox"
                      class="rounded cursor-pointer text-blue-600 border-gray-500 focus:ring-0 dark:bg-gray-700 dark:border-gray-600"
                      :checked="
                        selectedItems.some((obj) => obj?.id === item.id)
                      "
                    />
                  </button>
                </td>
                <td class="py-2 px-1 w-1.5">
                  <button
                    @click.stop
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                  >
                    <IconC
                      iconName="StarIcon"
                      iconType="outline"
                      iconClass="w-5 h-5"
                    />
                  </button>
                </td>
                <td class="py-2 px-3 w-1.5">
                  <button
                    @click.stop
                    class="p-3.5 rounded-full hover:bg-gray-200/50 dark:hover:bg-gray-800/50"
                  >
                    <IconC
                      iconName="BookmarkIcon"
                      iconType="outline"
                      iconClass="w-5 h-5 transform rotate-90"
                    />
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
      selectedItems: [],
      isTableLoading: true,
      currentPage: 1,
    };
  },
  computed: {
    notifications() {
      return this.$store.state.notificationsModule.notificationsList.data || [];
    },
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
  async created() {
    this.getNotifications(this.currentPage);
  },
  methods: {
    getNotifications(page) {
      this.$store
        .dispatch("notificationsModule/getNotificationsList", {
          per_page: 10,
          page: page,
        })
        .then(() => {
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
        read: !!this.selectedItems.find((x) => x.read === false),
      }));
      this.$store
        .dispatch("notificationsModule/updateNotifications", {
          notifications: this.selectedItems,
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
<style>
.shadow-inner-hover:hover {
  box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.5) !important;
}
</style>
