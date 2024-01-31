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
      </div>

      <div class="relative min-h-[350px] mt-5">
        <OverlayC :minHeight="`min-h-[350px]`" v-if="isFetching" />
        <apexchart
          v-if="!isFetching"
          width="100%"
          height="350"
          type="bar"
          :options="chartOptions"
          :series="chartSeries"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
import debounce from "lodash/debounce";
import RangeDateFilter from "@/components/RangeDateFilterComponent.vue";
export default {
  props: {
    dispatchModule: {
      type: String,
      required: true,
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
  components: {
    RangeDateFilter,
  },
  data() {
    return {
      isFetching: true,
      total_amountSold: "",
      currentDate: "",
      startDate: "",
      endDate: "",
      debouncedGetData: null,
    };
  },
  computed: {
    chartColumnWidth() {
      if (this.chartData.total_products <= 3) return "30%";
      else if (
        this.chartData.total_products > 3 &&
        this.chartData.total_products <= 6
      )
        return "60%";
      else return "95%";
    },
    chartSeries() {
      return this.chartData.series;
    },
    chartOptions() {
      const data = {
        colors: this.getColors(),
        chart: {
          type: "bar",
          height: 350,
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: this.chartColumnWidth,
          },
        },
        noData: {
          text: this.$t("missingChartData"),
          align: "center",
          verticalAlign: "middle",
          offsetX: 0,
          offsetY: 0,
          style: {
            color: "#7483A1",
            fontSize: "14px",
            fontFamily: undefined,
          },
        },
        xaxis: {
          categories: this.chartData.categories,
        },
        yaxis: [
          {
            title: {
              text: this.$t("quantity"),
            },
          },
          {
            opposite: true,
            title: {
              text: `${this.$t("total_amount")} (€)`,
            },
            labels: {
              formatter: function (value) {
                return `€${value.toFixed(2)}`;
              },
            },
          },
        ],
        tooltip: {
          y: {
            formatter: function (
              value,
              // eslint-disable-next-line no-unused-vars
              { series, seriesIndex, dataPointIndex, w }
            ) {
              if (seriesIndex === 1 || seriesIndex === 2) {
                return `€${value.toFixed(2)}`;
              }
              return value;
            },
            title: {
              formatter: (seriesName) => this.$t(seriesName) + ":",
            },
          },
        },
        legend: {
          formatter: (value) => this.$t(value),
        },
      };
      return data;
    },
  },
  watch: {
    startDate: {
      async handler() {
        if (this.endDate) this.debouncedGetData();
      },
    },
    endDate: {
      async handler() {
        if (this.startDate) this.debouncedGetData();
      },
    },
    id: {
      async handler() {
        if (this.startDate) this.getData();
      },
    },
  },
  created() {
    this.debouncedGetData = debounce(this.getData, 500);
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
        start_date: this.startDate,
        end_date: this.endDate,
      };
      await this.$store.dispatch(this.dispatchModule, data).then(() => {
        this.isFetching = false;
      });
      this.total_amountSold = parseFloat(
        this.chartData.series[0].data.reduce(
          (a, b) => parseFloat(a) + parseFloat(b),
          0
        )
      ).toFixed(2);
    },
    getColors() {
      const theme900 = getComputedStyle(document.body)
        .getPropertyValue("--color-theme-900")
        .replaceAll(" ", "");
      const theme600 = getComputedStyle(document.body)
        .getPropertyValue("--color-theme-600")
        .replaceAll(" ", "");
      const theme300 = getComputedStyle(document.body)
        .getPropertyValue("--color-theme-300")
        .replaceAll(" ", "");
      const theme = [theme900, theme600, theme300];

      const colors = [
        "#1d4ed8",
        "#93c5fd",
        "#b91c1c",
        "#fca5a5",
        "#7e22ce",
        "#d8b4fe",
      ];
      return [...theme, ...colors.filter((color) => !theme.includes(color))];
    },
  },
};
</script>
