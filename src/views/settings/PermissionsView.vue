<template>
  <div class="main-div">
    <div class="flex items-center justify-between mb-5">
      <h5
        class="text-3xl font-bold leading-none text-gray-900 dark:text-white flex items-center gap-2"
      >
        {{ $t("permissions") }}
        <button
          @mouseenter="() => (isInfoShowing = true)"
          @mouseleave="() => (isInfoShowing = false)"
        >
          <IconC iconName="InformationCircleIcon" iconClass="w-6 h-6" />
        </button>
      </h5>
      <button
        class="theme-gradient-btn flex items-center text-center"
        type="button"
        v-if="$store.state.userModule.currentUser.userRole === 'superadmin'"
        @click="$openModal(createRef)"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        New Permission
      </button>
    </div>
    <div
      class="p-4 border border-gray-300 rounded bg-neutral-50 dark:border-gray-600 dark:bg-neutral-700 transition duration-500"
      v-show="isInfoShowing"
    >
      <div class="flex items-center gap-2 text-gray-800 dark:text-gray-100">
        <IconC
          iconType="solid"
          iconName="InformationCircleIcon"
          iconClass="w-5 h-5"
        />
        <h3 class="text-lg font-medium">{{ $t("permissionsInfo") }}</h3>
      </div>
      <div class="mt-2 mb-4 text-sm text-gray-700 dark:text-gray-300">
        {{ $t("permissionsInfoText") }} <br />
        <div class="flex items-center gap-2">
          <p class="text-lg font-bold">{{ $t("subjects") }}:</p>
          {{ $t("subjectInfoText") }}
        </div>
        <p class="text-lg font-bold">{{ $t("actions") }}:</p>
        <ul class="list-disc list-inside">
          <li>
            <b>{{ $t("read") }}</b> - {{ $t("readPermissionText") }}
          </li>
          <li>
            <b>{{ $t("write") }}</b> - {{ $t("writePermissionText") }}
          </li>
          <li>
            <b>{{ $t("execute") }}</b> - {{ $t("executePermissionText") }}
          </li>
        </ul>
        <p class="mt-2">
          {{ $t("permissionsNoteText") }}
        </p>
      </div>
    </div>

    <div class="bg-transparent rounded-t-lg py-0 px-2 mb-3">
      <ul
        class="flex flex-wrap justify-center -mb-px text-sm font-medium text-center text-gray-500 dark:text-gray-400"
      >
        <li class="mr-2" @click="() => (activeTab = 'staff')">
          <p
            :class="
              activeTab === 'staff'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UserIcon" iconClass="w-6 h-6 mr-2" />
            {{ $t("staff") }}
          </p>
        </li>
        <li class="mr-2" @click="() => (activeTab = 'manager')">
          <p
            :class="
              activeTab === 'manager'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UsersIcon" iconClass="w-6 h-6 mr-2" />{{
              $t("manager")
            }}
          </p>
        </li>
        <li class="mr-2" @click="() => (activeTab = 'owner')">
          <p
            :class="
              activeTab === 'owner'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UserGroupIcon" iconClass="w-6 h-6 mr-2" />{{
              $t("owner")
            }}
          </p>
        </li>
        <li
          class="mr-2"
          @click="() => (activeTab = 'superadmin')"
          v-if="$store.state.userModule.currentUser.userRole === 'superadmin'"
        >
          <p
            :class="
              activeTab === 'superadmin'
                ? 'inline-flex items-center cursor-pointer p-4 text-theme-500 rounded-t-lg border-b-4 border-theme-500 active dark:text-theme-500 dark:border-theme-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UserGroupIcon" iconClass="w-6 h-6 mr-2" />{{
              $t("superadmin")
            }}
          </p>
        </li>
      </ul>
    </div>
    <div class="relative flex grow">
      <OverlayC v-if="isTableLoading" />
      <table class="w-full text-sm text-left rounded overflow-hidden relative">
        <thead
          class="text-md text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
        >
          <tr>
            <th scope="col" class="py-3 px-6">
              {{ $t("subject") }}
            </th>
            <th scope="col" class="py-3 px-3">
              {{ $t("action") }}
            </th>
            <th scope="col" class="py-3 px-3"></th>
          </tr>
        </thead>
        <tbody class="px-5">
          <template v-for="item in allPermissions" :key="item.id">
            <tr
              class="bg-white dark:text-gray-300 hover:text-black hover:dark:text-white border-b dark:bg-neutral-900 dark:border-gray-700"
            >
              <td class="py-2 px-6">
                {{ $t(item.subject) }}
              </td>
              <td class="py-2 px-3">{{ $t(item.action) }}</td>
              <td class="py-2 px-3 w-2 text-center">
                <label
                  :for="`toggle-${item.id}`"
                  class="inline-flex relative items-center cursor-pointer"
                  :class="{
                    'cursor-not-allowed': !$can('execute', 'permissions'),
                  }"
                  @click="
                    $can('execute', 'permissions') ? togglePermission(item) : ''
                  "
                >
                  <input
                    type="checkbox"
                    :id="`toggle-${item.id}`"
                    class="sr-only peer"
                    disabled
                    :checked="isActive(item.key)"
                    @click.stop
                  />
                  <div
                    class="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-theme-300 dark:peer-focus:ring-theme-800 rounded-full peer dark:bg-neutral-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-theme-600"
                  ></div>
                </label>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div
      :id="createRef"
      :ref="createRef"
      class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 w-full md:inset-0 h-modal md:h-full"
    >
      <div class="relative p-4 w-full max-w-lg h-full md:h-auto">
        <!-- Modal content -->
        <div class="relative bg-white rounded shadow dark:bg-neutral-700">
          <button
            type="button"
            class="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-neutral-200 hover:text-gray-900 rounded text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-neutral-800 dark:hover:text-white"
            @click="$hideModal(createRef)"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
            <span class="sr-only">Close modal</span>
          </button>
          <div class="py-6 px-6 lg:px-8">
            <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">
              {{
                $t("addNewResult", {
                  result: $t("permission").toLowerCase(),
                })
              }}
            </h3>
            <Form v-slot="{ errors }" @submit="createFunc" class="space-y-6">
              <div>
                <label
                  for="subject"
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                >
                  {{ $t("subject") }}</label
                >
                <Field
                  rules="required"
                  v-model="permission.subject"
                  type="text"
                  name="subject"
                  id="subject"
                  ref="subject"
                  class="default-input w-full"
                  :placeholder="$t('subject')"
                  required
                  :disabled="isLoading"
                />
                <span class="text-red-700">{{ errors.subject }}</span>
              </div>
              <div>
                <label
                  for="password"
                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                >
                  {{ $t("action") }}</label
                >
                <Field
                  rules="required"
                  v-model="permission.action"
                  type="text"
                  name="action"
                  id="action"
                  class="default-input w-full hidden"
                  disabled
                />
                <v-select
                  class="block w-full default-input !p-1"
                  v-model="permission.action"
                  :clearable="false"
                  :options="['read', 'write', 'execute']"
                  type="text"
                  name="action"
                  id="action"
                  label="option"
                  :placeholder="$t('action')"
                  required
                >
                  <template #selected-option="{ option }">
                    {{ $t(option) }}
                  </template>
                  <template #option="{ option }">
                    {{ $t(option) }}
                  </template>
                </v-select>
                <span class="text-red-700">{{ errors.action }}</span>
              </div>
              <button
                id="finish-sale-modal-btn"
                type="submit"
                class="inline-flex items-center justify-center w-full theme-gradient-btn"
              >
                <div role="status" v-if="isLoading">
                  <IconC
                    iconType="custom"
                    iconName="SpinnerIcon"
                    iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
                  />
                  <span class="sr-only">Loading...</span>
                </div>
                <template v-else>Submit</template>
              </button>
            </Form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { Field, Form } from "vee-validate";
export default {
  components: {
    Field,
    Form,
  },
  data() {
    return {
      activeTab: "staff",
      createRef: "createPermission",
      staffPermissions: [],
      managerPermissions: [],
      ownerPermissions: [],
      superadminPermissions: [],
      permission: {
        subject: "",
        action: "",
      },
      currentArr: [],
      isTableLoading: true,
      isInfoShowing: false,
      isLoading: false,
    };
  },
  async created() {
    await this.$store
      .dispatch("permissionsModule/getAllPermissions")
      .then(() => {
        this.isTableLoading = false;
      });
    await this.$store
      .dispatch("permissionsModule/getUserRolePermissions", "staff")
      .then((res) => {
        this.staffPermissions = res.data;
        this.currentArr = res.data;
      });
    await this.$store
      .dispatch("permissionsModule/getUserRolePermissions", "manager")
      .then((res) => {
        this.managerPermissions = res.data;
      });
    await this.$store
      .dispatch("permissionsModule/getUserRolePermissions", "owner")
      .then((res) => {
        this.ownerPermissions = res.data;
      });
    await this.$store
      .dispatch("permissionsModule/getUserRolePermissions", "superadmin")
      .then((res) => {
        this.superadminPermissions = res.data;
      });
  },
  watch: {
    activeTab: {
      handler(value) {
        this.currentArr = this[`${value}Permissions`];
      },
    },
  },
  computed: {
    allPermissions() {
      return this.$store.state.permissionsModule.allPermissions;
    },
    isActive() {
      return (key) => this.currentArr.some((x) => x.key === key);
    },
  },
  methods: {
    async togglePermission(item) {
      const data = {
        user_role: this.activeTab,
        key: item.key,
      };
      if (this.isActive(item.key)) {
        const idx = this.currentArr.findIndex((x) => x.key === item.key);
        this.currentArr.splice(idx, 1);
      } else {
        this.currentArr.push(item);
      }
      this.$store
        .dispatch("permissionsModule/updatePermission", data)
        .catch(async () => {
          await this.$toast.error(this.$t("somethingWrong"));
          if (this.isActive(item.key)) {
            const idx = this.currentArr.findIndex((x) => x.key === item.key);
            this.currentArr.splice(idx, 1);
          } else {
            this.currentArr.push(item);
          }
        });
    },
    createFunc() {
      const data = {
        user_role: this.$store.state.userModule.currentUser.userRole,
        ...this.permission,
      };
      this.isLoading = true;
      this.$store
        .dispatch("permissionsModule/createPermission", data)
        .then(async () => {
          this.$toast.success(this.$t("permissionCreatedSuccessfully"));
          await this.$store.dispatch("permissionsModule/getAllPermissions");
          this.isLoading = false;
          this.$hideModal(this.createRef);
          this.permission = { action: "", subject: "" };
        });
    },
  },
};
</script>
