import state from "./productModuleState";
import mutations from "./productModuleMutations";
import actions from "./productModuleActions";
import getters from "./productModuleGetters";

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
