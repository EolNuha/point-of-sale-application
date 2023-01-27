<template>
  <div class="bg-neutral-200 dark:bg-neutral-800 min-h-screen relative">
    <ul
      class="divide-x dark:divide-gray-800 flex flex-wrap items-center text-sm font-medium text-center text-gray-500 dark:text-gray-400 bg-white dark:bg-neutral-900 px-2 pt-2"
    >
      <li
        v-for="(tab, index) in tabs"
        :key="`tab-${index}`"
        class="relative"
        :class="tab === activeTab ? 'border-none' : ''"
      >
        <button
          @click="activeTab = tab"
          type="button"
          class="min-w-[150px] inline-flex justify-between items-center px-4 py-2"
          :class="
            tab === activeTab
              ? 'text-theme-600 bg-neutral-200 active dark:bg-neutral-800 dark:text-theme-500 relative rounded-t-lg'
              : 'hover:text-gray-600 hover:bg-neutral-50 dark:hover:bg-neutral-900/75 dark:hover:text-gray-300 bg-white dark:bg-neutral-900'
          "
        >
          <span>{{ $t("tab") }} {{ tab + 1 }}</span>
          <button
            v-if="tabs.length > 1"
            @click.stop="removeTab(index)"
            class="rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
          >
            <IconC
              iconType="solid"
              iconSize="20"
              iconName="XMarkIcon"
              iconClass="w-4 h-4"
            />
          </button>
        </button>
      </li>
      <li
        class="pl-2"
        :id="`add-tab-tooltip-btn`"
        @mouseover="
          $showTooltip({
            targetEl: `add-tab-tooltip`,
            triggerEl: `add-tab-tooltip-btn`,
          })
        "
      >
        <button
          @click="addTab()"
          type="button"
          class="p-1.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700 flex items-center gap-2"
          :disabled="tabs.length >= 5"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5" />
        </button>
      </li>
      <div
        :id="`add-tab-tooltip`"
        role="tooltip"
        class="inline-block absolute invisible z-10 py-2 px-3 text-sm font-medium text-white bg-neutral-700 rounded shadow-sm opacity-0 tooltip"
      >
        {{ tabs.length >= 5 ? $t("maxTabs") : $t("addTab") }}
      </div>
    </ul>
    <template v-for="tab in tabs" :key="tab">
      <sale-tab v-show="tab === activeTab" :id="tab" />
    </template>
  </div>
</template>

<script>
import SaleTab from "./SaleTab.vue";
export default {
  components: {
    SaleTab,
  },
  name: "NewSaleView",
  data() {
    return {
      activeTab: this.$store.state.saleModule.currentTabs[0] || 0,
    };
  },
  // async beforeRouteLeave(to, from, next) {
  //   if (!(this.products?.length === 0)) {
  //     const options = this.$swalConfirmObject();
  //     options.html = `<p class='text-gray-500 dark:text-gray-300'>${this.$t(
  //       "saleNotFinished"
  //     )}</p>`;
  //     options.icon = "info";
  //     options.position = "top";
  //     await this.$swal(options).then((result) => {
  //       if (result.isDenied || result.isDismissed) {
  //         return;
  //       } else {
  //         next();
  //       }
  //     });
  //   } else {
  //     next();
  //   }
  // },
  computed: {
    tabs: {
      get() {
        return this.$store.state.saleModule.currentTabs;
      },
      set() {},
    },
    sales: {
      get() {
        return this.$store.state.saleModule.currentSales;
      },
      set() {},
    },
  },
  methods: {
    addTab() {
      const lastTab = this.tabs[this.tabs.length - 1];
      this.tabs.push(lastTab + 1);
      this.sales.push({ tab: lastTab + 1, products: [] });
      this.activeTab = this.tabs[this.tabs.length - 1];
    },
    removeTab(idx) {
      const saleIdx = this.sales.findIndex((x) => x.tab === this.tabs[idx]);
      this.sales.splice(saleIdx, 1);
      const tabIdx = this.tabs.indexOf(this.activeTab);
      this.tabs.splice(idx, 1);
      if (idx === tabIdx) this.activeTab = this.tabs[this.tabs.length - 1];
    },
  },
};
</script>
