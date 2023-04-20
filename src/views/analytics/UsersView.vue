<template>
  <div
    class="bg-neutral-200 dark:bg-neutral-800 min-h-screen p-4 flex flex-col gap-4"
  >
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getUsersSaleRevenue`"
      :chartData="$store.state.analyticsModule.usersRevenue"
      :titleContent="$t('topEmployees')"
      :textContent="$t('topUsersMostRevenue')"
    >
    </AreaChartMoney>
    <AreaChartMoney
      :dispatchModule="`analyticsModule/getUserStats`"
      :id="selectedUser.id"
      :chartData="$store.state.analyticsModule.userStats"
      :titleContent="`${$t('user')}: ${selectedUser.firstName} ${
        selectedUser.lastName
      }`"
      :textContent="$t('revenueMade')"
    >
      <div
        class="flex flex-row flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">{{ $t("user") }}:</span>
        <v-select
          class="w-full min-w-[150px] md:w-[200px] default-input"
          v-model="selectedUser"
          @search="($event, loading) => searchUsers($event, loading)"
          :value="users"
          :options="users"
          :clearable="false"
          :filterable="false"
          :reduce="(users) => users"
          label="firstName"
        >
          <template #selected-option="{ firstName, lastName }">
            {{ firstName }} {{ lastName }}
          </template>
          <template #option="{ firstName, lastName }">
            {{ firstName }} {{ lastName }}
          </template>
        </v-select>
      </div>
    </AreaChartMoney>
  </div>
</template>
<script>
import AreaChartMoney from "@/components/analytics/AreaChartMoney.vue";
export default {
  components: {
    AreaChartMoney,
  },
  data() {
    return {
      isFetching: true,
      startDate: "",
      endDate: "",
      selectedUser: {},
      search: "",
    };
  },
  watch: {
    "$store.state.userModule.currentUser": function () {
      this.selectedUser = this.$store.state.userModule.currentUser;
    },
  },
  computed: {
    users() {
      return this.$store.getters["userModule/getUsersList"];
    },
  },
  created() {
    this.getUsers(this.search).then(() => {
      this.selectedUser = this.users[0];
    });
  },
  methods: {
    async searchUsers(search, loading) {
      this.search = search;
      loading(true);
      await this.getUsers(search);
      loading(false);
    },
    async getUsers(search) {
      await this.$store.dispatch("userModule/getUsers", {
        page: 1,
        per_page: 20,
        sort_column: "first_name",
        sort_dir: "asc",
        search: search,
      });
    },
  },
};
</script>
