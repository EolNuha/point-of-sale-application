<template>
  <div class="flex-col flex bg-gray-200 dark:bg-neutral-800 min-h-screen p-4">
    <h5
      class="text-3xl font-bold leading-none text-gray-900 dark:text-white mb-5 flex items-center gap-2"
    >
      {{ $t("permissions") }}
      <button
        @mouseenter="() => (isInfoShowing = true)"
        @mouseleave="() => (isInfoShowing = false)"
      >
        <IconC iconName="InformationCircleIcon" iconClass="w-6 h-6" />
      </button>
    </h5>
    <div
      class="p-4 border border-gray-300 rounded-lg bg-gray-50 dark:border-gray-600 dark:bg-neutral-700 transition duration-500"
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
        <li
          class="mr-2"
          @click="
            () => (
              (activeTab = 'staff'), (colName = null), (selectedItems = [])
            )
          "
        >
          <p
            :class="
              activeTab === 'staff'
                ? 'inline-flex items-center cursor-pointer p-4 text-blue-500 rounded-t-lg border-b-4 border-blue-500 active dark:text-blue-500 dark:border-blue-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UserIcon" iconClass="w-6 h-6 mr-2" />
            {{ $t("staff") }}
          </p>
        </li>
        <li
          class="mr-2"
          @click="
            () => (
              (activeTab = 'manager'), (colName = 'star'), (selectedItems = [])
            )
          "
        >
          <p
            :class="
              activeTab === 'manager'
                ? 'inline-flex items-center cursor-pointer p-4 text-blue-500 rounded-t-lg border-b-4 border-blue-500 active dark:text-blue-500 dark:border-blue-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UsersIcon" iconClass="w-6 h-6 mr-2" />{{
              $t("manager")
            }}
          </p>
        </li>
        <li
          class="mr-2"
          @click="
            () => (
              (activeTab = 'owner'), (colName = 'read'), (selectedItems = [])
            )
          "
        >
          <p
            :class="
              activeTab === 'owner'
                ? 'inline-flex items-center cursor-pointer p-4 text-blue-500 rounded-t-lg border-b-4 border-blue-500 active dark:text-blue-500 dark:border-blue-500 group'
                : 'inline-flex items-center cursor-pointer p-4 rounded-t-lg border-b-4 border-transparent hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group'
            "
          >
            <IconC iconName="UserGroupIcon" iconClass="w-6 h-6 mr-2" />{{
              $t("owner")
            }}
          </p>
        </li>
      </ul>
    </div>
    <div>
      <table class="w-full text-sm text-left relative">
        <OverlayC v-if="isTableLoading" />
        <thead
          class="text-md text-gray-700 uppercase bg-gray-100 dark:bg-neutral-700 dark:text-gray-400 cursor-default"
        >
          <tr>
            <th scope="col" class="py-3 px-6">{{ $t("subject") }}</th>
            <th scope="col" class="py-3 px-3">{{ $t("action") }}</th>
            <th
              scope="col"
              class="py-3 px-3"
              v-if="$can('execute', 'permissions')"
            ></th>
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
              <td
                class="py-2 px-3 w-2 text-center"
                v-if="$can('execute', 'permissions')"
              >
                <label
                  :for="`toggle-${item.id}`"
                  class="inline-flex relative items-center cursor-pointer"
                  @click="togglePermission(item)"
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
                    class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-neutral-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
                  ></div>
                </label>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      activeTab: "staff",
      staffPermissions: [],
      managerPermissions: [],
      ownerPermissions: [],
      currentArr: [],
      isTableLoading: true,
      isInfoShowing: false,
    };
  },
  async created() {
    await this.$store
      .dispatch("permissionsModule/getAllPermissions")
      .then(() => {
        this.isTableLoading = false;
      });
    await this.$store
      .dispatch("permissionsModule/getUserTypePermissions", "staff")
      .then((res) => {
        this.staffPermissions = res.data;
        this.currentArr = res.data;
      });
    await this.$store
      .dispatch("permissionsModule/getUserTypePermissions", "manager")
      .then((res) => {
        this.managerPermissions = res.data;
      });
    await this.$store
      .dispatch("permissionsModule/getUserTypePermissions", "owner")
      .then((res) => {
        this.ownerPermissions = res.data;
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
        user_type: this.activeTab,
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
  },
};
</script>
