import Icon from "@/components/icons/IconComponent.vue";
import Overlay from "@/components/OverlayComponent.vue";
import Pagination from "@/components/PaginationComponent.vue";
import EmptyResults from "@/components/EmptyResultsComponent.vue";
import vSelect from "vue-select";

const registerComponents = (app) => {
  app
    .component("IconC", Icon)
    .component("OverlayC", Overlay)
    .component("PaginationC", Pagination)
    .component("EmptyResultsC", EmptyResults)
    .component("v-select", vSelect);
};

export default registerComponents;
