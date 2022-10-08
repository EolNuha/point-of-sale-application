import state from "./userModuleState";
import mutations from "./userModuleMutations";
import actions from "./userModuleActions";
import getters from "./userModuleGetters";

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
