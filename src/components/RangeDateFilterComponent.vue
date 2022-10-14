<template>
  <div>
    <div class="flex items-center gap-2 flex-wrap sm:flex-nowrap">
      <v-select
        class="w-[150px] md:w-[200px] default-input"
        v-model="currentDate"
        :value="ranges"
        :options="ranges"
        :clearable="false"
        :reduce="(ranges) => ranges.id"
        label="value"
      ></v-select>

      <div class="flex items-center gap-2 w-full" v-if="currentDate === null">
        <input
          v-model="startDate"
          ref="startDate"
          name="start"
          type="date"
          class="w-full default-input"
          placeholder="Select date start"
          :max="endDate"
        />
        <span class="text-gray-500">to</span>
        <input
          v-model="endDate"
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
        { id: 0, value: "Today" },
        { id: 7, value: "Last 7 days" },
        { id: 30, value: "Last 30 days" },
        { id: 60, value: "Last 60 days" },
        { id: 90, value: "Last 90 days" },
        { id: 365, value: "Last 12 months" },
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
      const date = new Date();
      date.setDate(date.getDate() - days);
      const startDate = this.formatDate(date);
      const endDate = this.formatDate(new Date());

      return { startDate, endDate };
    },
  },
};
</script>
