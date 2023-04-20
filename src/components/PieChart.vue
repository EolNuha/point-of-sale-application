<template>
  <apexchart
    width="100%"
    height="350"
    type="pie"
    :options="options"
    :series="series"
  ></apexchart>
</template>

<script>
export default {
  props: ["chartData"],
  data() {
    return {
      options: {},
      series: [],
      chartColor: "",
    };
  },
  created() {
    this.options = {
      type: "pie",
      // orange "#fdba8c",
      // colors: this.getColors(),
      chart: {
        id: this.chartData.info.chartName,
      },
      labels: this.chartData.options,
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
      tooltip: {
        enabled: true,
        enabledOnSeries: true,
        followCursor: false,
        style: {
          fontSize: "16px",
        },
        x: {
          show: true,
          format: "dd MMM",
        },
        y: {
          formatter: function (value) {
            return value + "€";
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
    const series = this.chartData.series[0]?.data?.map((item) => Number(item));
    this.series = series;
  },
  methods: {
    getColors() {
      const theme500 = getComputedStyle(document.body)
        .getPropertyValue("--color-theme-700")
        .replaceAll(" ", "");
      const theme300 = getComputedStyle(document.body)
        .getPropertyValue("--color-theme-300")
        .replaceAll(" ", "");
      const theme = [theme500, theme300];

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

<style lang="scss">
@import "/src/styles/components/_chart.scss";
</style>
