<template>
  <apexchart
    width="100%"
    height="350"
    type="area"
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
    };
  },
  async created() {
    this.options = {
      colors: ["#008ffb", "#fdba8c"],
      chart: {
        id: this.chartData.info.chartName,
      },
      xaxis: {
        categories: this.chartData.options,
      },
      dataLabels: {
        enabled: false,
      },
      markers: {
        size: 5,
        strokeWidth: 3,
      },
      noData: {
        text: "There is missing data for this chart.",
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
          formatter: undefined,
        },
        y: {
          formatter: function (value) {
            return value + "€";
          },
          title: {
            formatter: (seriesName) => seriesName,
          },
        },
      },
    };
    this.series = this.chartData.series;
  },
};
</script>

<style lang="scss">
@import "/src/styles/components/_chart.scss";
</style>
