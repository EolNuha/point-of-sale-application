import Ability from "@/services/ability";
export default {
  methods: {
    async setUserData() {
      await this.$store.dispatch("permissionsModule/getUserPermissions");
      const data = {
        user: this.$store.state.userModule.currentUser,
        ability: this.$store.state.permissionsModule.permissions,
      };

      Ability.update(data.ability);
      localStorage.setItem("userData", JSON.stringify(data));
    },
  },
};
