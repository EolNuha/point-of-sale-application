<template>
  <div class="bg-white dark:bg-neutral-900 rounded relative">
    <div
      class="flex items-center rounded-t flex-row flex-wrap lg:flex-nowrap justify-between p-3 px-8 gap-2 bg-neutral-100 dark:bg-neutral-700/75"
    >
      <div
        class="w-full flex flex-column items-center gap-2 text-gray-700 dark:text-gray-200"
      >
        <span class="font-bold">{{ $t("date") }}:</span>
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
          class="w-[150px] md:w-[200px] default-input"
          placeholder="Select date start"
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
            {{ titleContent }} {{ startDate }}
          </h3>
          <p class="text-gray-500 dark:text-gray-400">
            {{ textContent }}
            <b>{{ $t("on") }} {{ startDate }}</b>
          </p>
        </div>
        <div
          class="inline-flex flex-col items-center text-green-500"
          v-if="!isFetching"
        >
          <h3 class="text-3xl text-gray-900 dark:text-white">
            {{ Number(chartData.info.currTotal).toFixed(2) }}€
          </h3>
          <slot name="totalExtra"></slot>
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
import AreaChart from "@/components/AreaChart.vue";
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
  components: { AreaChart },
  data() {
    return {
      isFetching: true,
      totalAmountSold: "",
      startDate: "",
    };
  },
  watch: {
    startDate: {
      async handler() {
        this.getData();
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
  created() {
    this.startDate = this.formatDate(new Date());
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
