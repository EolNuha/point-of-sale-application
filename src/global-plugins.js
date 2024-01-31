import focusPlugin from "./plugins/focus";
import swalPlugin from "./plugins/swal";
import customPlugins from "./plugins/custom";
import flowbitePlugings from "./plugins/flowbite";

const registerPlugins = (app) => {
  app.use(focusPlugin).use(swalPlugin).use(customPlugins).use(flowbitePlugings);
};

export default registerPlugins;
