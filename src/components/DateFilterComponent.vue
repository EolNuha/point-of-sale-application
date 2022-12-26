<template>
  <div
    class="flex items-center my-3 gap-2 search-input-width flex-wrap sm:flex-nowrap"
  >
    <v-select
      class="w-full sm:w-1/2 md:w-1/3 default-input"
      v-model="currentMonth"
      :value="months"
      :options="months"
      :clearable="false"
      :reduce="(months) => months.id"
      label="value"
    ></v-select>

    <div class="flex items-center gap-2 w-full" v-if="currentMonth === 0">
      <input
        @input="
          $debounce(() => {
            dateStart = $event.target.value;
          })
        "
        :value="dateStart"
        ref="startDate"
        name="start"
        type="date"
        class="w-full default-input"
        placeholder="Select date start"
        :max="dateEnd"
      />
      <span class="text-gray-500">{{ $t("to") }}</span>
      <input
        @input="
          $debounce(() => {
            dateEnd = $event.target.value;
          })
        "
        :value="dateEnd"
        ref="endDate"
        name="start"
        type="date"
        class="w-full default-input"
        placeholder="Select date end"
        :min="dateStart"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    startDate: String,
    endDate: String,
    dispatchModule: String,
    searchQuery: String,
  },
  data() {
    return {
      months: [
        { id: 0, value: "Custom" },
        { id: 1, value: this.$t("january") },
        { id: 2, value: this.$t("february") },
        { id: 3, value: this.$t("march") },
        { id: 4, value: this.$t("april") },
        { id: 5, value: this.$t("may") },
        { id: 6, value: this.$t("june") },
        { id: 7, value: this.$t("july") },
        { id: 8, value: this.$t("august") },
        { id: 9, value: this.$t("september") },
        { id: 10, value: this.$t("october") },
        { id: 11, value: this.$t("november") },
        { id: 12, value: this.$t("december") },
      ],
      currentMonth: "",
      dateStart: this.startDate,
      dateEnd: this.endDate,
    };
  },
  watch: {
    currentMonth: {
      async handler(value) {
        if (value !== 0) {
          const month = String(value).padStart(2, "0");
          const year = new Date().getFullYear();
          const days = String(new Date(year, month, 0).getDate()).padStart(
            2,
            "0"
          );
          this.dateStart = `${year}-${month}-01`;
          this.dateEnd = `${year}-${month}-${days}`;
        }
      },
    },
    dateStart: {
      async handler(value) {
        this.$emit("startDateChange", value);
        this.$emit("isTableLoading", true);
        const idx = this.$checkIfMonth(value, this.dateEnd);
        if (idx !== -1) {
          this.currentMonth = idx + 1;
        } else {
          this.currentMonth = 0;
        }
        this.$store
          .dispatch(this.dispatchModule, {
            startDate: value,
            endDate: this.dateEnd,
            page: 1,
            search: this.searchQuery,
          })
          .then(() => {
            this.$emit("isTableLoading", false);
          })
          .catch(() => {
            this.$emit("isTableLoading", false);
            this.$toast.error(this.$t("somethingWrong"));
          });
      },
    },
    dateEnd: {
      async handler(value) {
        this.$emit("endDateChange", value);
        this.$emit("isTableLoading", true);
        const idx = this.$checkIfMonth(this.dateStart, value);
        if (idx !== -1) {
          this.currentMonth = idx + 1;
        } else {
          this.currentMonth = 0;
        }
        this.$store
          .dispatch(this.dispatchModule, {
            startDate: this.dateStart,
            endDate: value,
            page: 1,
            search: this.searchQuery,
          })
          .then(() => {
            this.$emit("isTableLoading", false);
          })
          .catch(() => {
            this.$emit("isTableLoading", false);
            this.$toast.error(this.$t("somethingWrong"));
          });
      },
    },
  },
  created() {
    this.currentMonth = new Date().getMonth() + 1;
  },
};
</script>
