<template>
  <div>
    <div class="flex items-center gap-2 flex-wrap md:flex-nowrap">
      <v-select
        class="w-full min-w-[150px] sm:w-[200px] default-input"
        v-model="currentDate"
        :value="ranges"
        :options="ranges"
        :clearable="false"
        :reduce="(ranges) => ranges.id"
        label="value"
      ></v-select>

      <div
        class="flex items-center flex-wrap md:flex-nowrap gap-2 w-full"
        v-if="currentDate === null"
      >
        <input
          @input="
            $debounce(() => {
              startDate = $event.target.value;
            })
          "
          :value="startDate"
          ref="startDate"
          name="start"
          type="date"
          class="w-full default-input"
          placeholder="Select date start"
          :max="endDate"
        />
        <span class="text-gray-500">{{ $t("to") }}</span>
        <input
          @input="
            $debounce(() => {
              endDate = $event.target.value;
            })
          "
          :value="endDate"
          ref="endDate"
          name="start"
          type="date"
          class="w-full default-input"
          placeholder="Select date end"
          :min="startDate"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ranges: [
        { id: null, value: "Custom" },
        { id: 0, value: this.$t("today") },
        { id: 7, value: this.$t("last7days") },
        { id: 30, value: this.$t("last30days") },
        { id: 60, value: this.$t("last60days") },
        { id: 90, value: this.$t("last90days") },
        { id: 365, value: this.$t("last12months") },
      ],
      currentDate: "",
      startDate: "",
      endDate: "",
    };
  },
  watch: {
    currentDate: {
      async handler(value) {
        if (value !== null) {
          this.$emit(
            "currentDateChange",
            this.ranges.filter((obj) => {
              return obj.id === value;
            })[0].value
          );
          const dates = this.getDates(value);
          this.startDate = dates.startDate;
          this.endDate = dates.endDate;
        } else {
          this.$emit("currentDateChange", null);
        }
      },
    },
    startDate: {
      async handler(value) {
        this.$emit("startDateChange", value);
      },
    },
    endDate: {
      async handler(value) {
        this.$emit("endDateChange", value);
      },
    },
  },
  created() {
    this.currentDate = 7;
  },
  methods: {
    formatDate(date) {
      return (
        String(date.getFullYear()).padStart(2, "0") +
        "-" +
        String(date.getMonth() + 1).padStart(2, "0") +
        "-" +
        String(date.getDate()).padStart(2, "0")
      );
    },
    getDates(days) {
      if (days !== 0) days--;
      const date = new Date();
      date.setDate(date.getDate() - days);
      const startDate = this.formatDate(date);
      const endDate = this.formatDate(new Date());

      return { startDate, endDate };
    },
  },
};
</script>
