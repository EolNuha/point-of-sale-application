<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl my-5 py-8 relative px-5">
    <div
      class="flex items-center flex-row flex-wrap sm:flex-nowrap justify-between px-3 gap-2"
    >
      <div class="w-full">
        <RangeDateFilter
          @startDateChange="startDate = $event"
          @endDateChange="endDate = $event"
          @currentDateChange="currentDate = $event"
        />
      </div>
      <slot></slot>
    </div>
    <!-- from: ${this.startDate} to: ${this.endDate} -->
    <div class="flex items-center justify-between px-3">
      <div>
        <h3 class="text-gray-900 dark:text-white text-3xl">
          {{ titleContent }}
        </h3>
        <p class="text-gray-500 dark:text-gray-400">
          {{ textContent }}
          <b>{{ setCurrentDateText(currentDate) }}</b>
        </p>
      </div>
      <div class="inline-flex items-center text-green-500 text-3xl">
        <IconC iconName="ArrowLongUpIcon" iconClass="w-8 h-8" />
        {{ totalAmountSold }}€
      </div>
    </div>

    <div class="relative min-h-[350px]">
      <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetching" />
      <AreaChart v-if="!isFetching" :chartData="chartData" />
    </div>
  </div>
</template>
<script>
export default {
  props: {
    dispatchModule: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: false,
      default: null,
    },
    chartData: {
      type: null,
      required: true,
    },
    titleContent: {
      type: String,
      required: true,
    },
    textContent: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isFetching: true,
      totalAmountSold: "",
      currentDate: "",
      startDate: "",
      endDate: "",
    };
  },
  watch: {
    startDate: {
      async handler() {
        if (this.endDate) this.getData();
      },
    },
    endDate: {
      async handler() {
        if (this.startDate) this.getData();
      },
    },
    id: {
      async handler() {
        if (this.startDate) this.getData();
      },
    },
  },
  methods: {
    setCurrentDateText(e) {
      if (e === "Today") return "today";
      if (e && e !== "Today") return `in the ${e.toLowerCase()}`;
      if (!e) return `from: ${this.startDate} to: ${this.endDate}`;
    },
    async getData() {
      this.isFetching = true;
      const data = {
        startDate: this.startDate,
        endDate: this.endDate,
        id: this.id,
      };
      await this.$store.dispatch(this.dispatchModule, data).then(() => {
        this.isFetching = false;
      });
      this.totalAmountSold = parseFloat(
        this.chartData.series.reduce((a, b) => parseFloat(a) + parseFloat(b), 0)
      ).toFixed(2);
    },
  },
};
</script>
