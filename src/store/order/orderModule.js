import state from "./orderModuleState";
import mutations from "./orderModuleMutations";
import actions from "./orderModuleActions";
import getters from "./orderModuleGetters";

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
