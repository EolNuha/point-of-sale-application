<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl my-5 relative">
    <div
      class="flex items-center rounded-t-xl flex-row flex-wrap lg:flex-nowrap justify-between p-3 sm:px-8 gap-2 bg-gray-100 dark:bg-gray-700/75 relative"
    >
      <div
        class="w-full flex flex-column flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">Date:</span>
        <RangeDateFilter
          @startDateChange="startDate = $event"
          @endDateChange="endDate = $event"
          @currentDateChange="currentDate = $event"
        />
      </div>
      <slot></slot>
    </div>
    <!-- from: ${this.startDate} to: ${this.endDate} -->
    <div class="p-5">
      <div
        class="flex items-center justify-between px-3 flex-wrap sm:flex-nowrap gap-2"
      >
        <div>
          <h3 class="text-gray-900 dark:text-white text-3xl">
            {{ titleContent }}
          </h3>
          <p class="text-gray-500 dark:text-gray-400">
            {{ textContent }}
            <b>{{ setCurrentDateText(currentDate) }}</b>
          </p>
        </div>
        <div class="inline-flex items-center flex-col" v-if="!isFetching">
          <h3 class="text-3xl text-gray-900 dark:text-white">
            {{ chartData.info.currTotal }}€
          </h3>
          <p
            class="inline-flex items-center text-green-500"
            v-if="chartData.info.percentageDiff > 0"
          >
            +{{ chartData.info.percentageDiff }}%<IconC
              iconName="ArrowLongUpIcon"
              iconClass="w-5 h-5"
            />
          </p>
          <p
            class="inline-flex items-center text-gray-500"
            v-if="chartData.info.percentageDiff === 0"
          >
            {{ chartData.info.percentageDiff }}%<IconC
              iconName="ArrowLongUpIcon"
              iconClass="w-5 h-5"
            />
          </p>
          <p
            class="inline-flex items-center text-red-700"
            v-if="chartData.info.percentageDiff < 0"
          >
            {{ chartData.info.percentageDiff }}%
          </p>
        </div>
      </div>

      <div class="relative min-h-[350px] mt-5">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetching" />
        <AreaChart v-if="!isFetching" :chartData="chartData" />
      </div>
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
      type: Number,
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
        this.chartData.series[0].data.reduce(
          (a, b) => parseFloat(a) + parseFloat(b),
          0
        )
      ).toFixed(2);
    },
  },
};
</script>
