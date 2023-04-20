<template>
  <div class="bg-white dark:bg-neutral-900 rounded relative">
    <div
      class="flex items-center rounded-t flex-row flex-wrap lg:flex-nowrap justify-between p-3 sm:px-8 gap-2 bg-neutral-100 dark:bg-neutral-700/75 relative"
    >
      <div
        class="w-full flex flex-column flex-wrap sm:flex-nowrap items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">{{ $t("date") }}:</span>
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
            {{ Number(chartData?.info?.currTotal).toFixed(2) }}€
          </h3>
          <p
            class="inline-flex items-center text-green-500"
            v-if="chartData?.info?.percentageDiff > 0"
          >
            +{{ chartData?.info?.percentageDiff }}%<IconC
              iconName="ArrowLongUpIcon"
              iconClass="w-5 h-5"
            />
          </p>
          <p
            class="inline-flex items-center text-gray-500"
            v-if="chartData?.info?.percentageDiff === 0"
          >
            {{ chartData?.info?.percentageDiff }}%
          </p>
          <p
            class="inline-flex items-center text-red-700"
            v-if="chartData?.info?.percentageDiff < 0"
          >
            {{ chartData?.info?.percentageDiff }}%<IconC
              iconName="ArrowLongDownIcon"
              iconClass="w-5 h-5"
            />
          </p>
        </div>
      </div>

      <div class="relative min-h-[350px] mt-5">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetching" />
        <AreaChart
          v-if="!isFetching && chartType === 'area'"
          :chartData="chartData"
        />
        <PieChart
          v-if="!isFetching && chartType === 'pie'"
          :chartData="chartData"
        />
      </div>
    </div>
  </div>
</template>
<script>
import AreaChart from "@/components/AreaChart.vue";
import PieChart from "@/components/PieChart.vue";
import RangeDateFilter from "@/components/RangeDateFilterComponent.vue";
export default {
  props: {
    dispatchModule: {
      type: String,
      required: true,
    },
    id: {
      type: null,
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
    chartType: {
      type: String,
      required: false,
      default: "area",
    },
  },
  components: {
    RangeDateFilter,
    AreaChart,
    PieChart,
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
    "$i18n.locale": {
      async handler() {
        this.isFetching = true;
        await setTimeout(() => {}, 100);
        this.isFetching = false;
      },
    },
  },
  methods: {
    setCurrentDateText(e) {
      if (e === "Today" || e === "Sot") return this.$t("today").toLowerCase();
      if (e && e !== "Today") return `${this.$t("inThe")} ${e.toLowerCase()}`;
      if (!e)
        return `${this.$t("from")}: ${this.startDate} ${this.$t("to")}: ${
          this.endDate
        }`;
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
