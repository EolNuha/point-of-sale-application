import Icon from "@/components/icons/IconComponent.vue";
import Overlay from "@/components/OverlayComponent.vue";
import Pagination from "@/components/PaginationComponent.vue";
import EmptyResults from "@/components/EmptyResultsComponent.vue";
import DateFilter from "@/components/DateFilterComponent.vue";
import RangeDateFilter from "@/components/RangeDateFilterComponent.vue";
import AreaChart from "@/components/AreaChart.vue";
import vSelect from "vue-select";

const registerComponents = (app) => {
  app
    .component("IconC", Icon)
    .component("OverlayC", Overlay)
    .component("PaginationC", Pagination)
    .component("EmptyResultsC", EmptyResults)
    .component("DateFilter", DateFilter)
    .component("RangeDateFilter", RangeDateFilter)
    .component("AreaChart", AreaChart)
    .component("v-select", vSelect);
};

export default registerComponents;
