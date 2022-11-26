import focusPlugin from "./plugins/focus";
import debouncePlugin from "./plugins/debounce";
import swalPlugin from "./plugins/swal";
import customPlugins from "./plugins/custom";
import flowbitePlugings from "./plugins/flowbite";

const registerPlugins = (app) => {
  app
    .use(focusPlugin)
    .use(debouncePlugin)
    .use(swalPlugin)
    .use(customPlugins)
    .use(flowbitePlugings);
};

export default registerPlugins;
