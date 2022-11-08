import { Ability } from "@casl/ability";
const storedAbilities = localStorage.getItem("userData");
const abilities = JSON.parse(storedAbilities)?.ability || [];
export default new Ability(abilities);
