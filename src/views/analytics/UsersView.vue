<template>
  <div class="bg-gray-200 dark:bg-gray-800 min-h-screen px-4">
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
          :value="users"
          :options="users"
          :clearable="false"
          :reduce="(users) => users"
          label="firstName"
        ></v-select>
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
    this.$store.dispatch("userModule/getUsers", {
      page: 1,
      per_page: 1000000000,
    });
    this.selectedUser = this.$store.state.userModule.currentUser;
  },
};
</script>
