import openModalPlugin from "./plugins/modals";
import focusPlugin from "./plugins/focus";
import tooltipsPlugin from "./plugins/tooltips";
import dropdownPlugin from "./plugins/dropdown";
import debouncePlugin from "./plugins/debounce";
import swalPlugin from "./plugins/swal";
import customPlugins from "./plugins/custom";

const registerPlugins = (app) => {
  app
    .use(openModalPlugin)
    .use(focusPlugin)
    .use(tooltipsPlugin)
    .use(dropdownPlugin)
    .use(debouncePlugin)
    .use(swalPlugin)
    .use(customPlugins);
};

export default registerPlugins;
