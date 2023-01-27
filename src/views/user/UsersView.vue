<!-- eslint-disable no-undef -->
<template>
  <div class="main-div">
    <div class="full-layout flex flex-col">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center search-input-width">
          <label for="simple-search" class="sr-only">{{ $t("search") }}</label>
          <div class="relative w-full">
            <div
              class="flex absolute inset-y-0 left-0 items-center pl-3 pointer-events-none"
            >
              <IconC
                iconType="solid"
                iconName="MagnifyingGlassIcon"
                iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
              />
            </div>
            <input
              @input="
                $debounce(() => {
                  searchQuery = $event.target.value;
                })
              "
              type="text"
              class="default-input w-full px-10"
              :placeholder="$t('search')"
            />
            <div
              v-if="showFilters"
              class="flex absolute inset-y-0 right-10 items-center pr-3 pointer-cursor"
            >
              <v-select
                class="min-w-[8rem] w-fit default-input"
                v-model="isActiveFilters"
                :placeholder="$t('status')"
                :options="[
                  { name: $t('active'), value: true },
                  { name: $t('inactive'), value: false },
                ]"
                :reduce="(options) => options.value"
                :clearable="false"
                :multiple="true"
                label="name"
              ></v-select>
            </div>
            <button
              class="flex absolute inset-y-0 right-0 items-center pointer-cursor p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-600"
              @click="showFilters = !showFilters"
            >
              <IconC
                v-if="!showFilters"
                iconName="FunnelIcon"
                iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
              />
              <IconC
                v-else
                iconName="XMarkIcon"
                iconClass="w-5 h-5 text-gray-500 dark:text-gray-400"
              />
            </button>
          </div>
        </div>
        <button
          v-if="$can('write', 'users')"
          @click="
            $router.push({
              name: 'new-user',
            })
          "
          class="theme-gradient-btn flex items-center text-center"
        >
          <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
          {{ $t("createNewUser") }}
        </button>
      </div>

      <div class="overflow-hidden rounded my-5 flex grow relative">
        <div class="overflow-x-auto overflow-y-hidden scrollbar-style grow">
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="users?.length === 0 && !isTableLoading"
            pluralText="Users"
            singularText="User"
            :search="searchQuery"
            routeName="new-user"
          />
          <table
            class="bg-white dark:bg-neutral-800 w-full text-sm text-left text-gray-700 dark:text-gray-400"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-neutral-100 dark:bg-neutral-700 dark:text-gray-400"
            >
              <tr>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('id')"
                >
                  <div class="flex justify-between items-center">
                    ID
                    <template v-if="sortColumn === 'id'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('first_name')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("firstName") }}
                    <template v-if="sortColumn === 'first_name'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('last_name')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("lastName") }}
                    <template v-if="sortColumn === 'last_name'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('username')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("username") }}
                    <template v-if="sortColumn === 'username'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('email')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("email") }}
                    <template v-if="sortColumn === 'email'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('user_role')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("type") }}
                    <template v-if="sortColumn === 'user_role'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6 hover:bg-neutral-200/[.6] hover:dark:bg-neutral-600"
                  @click="sort('active')"
                >
                  <div class="flex justify-between items-center">
                    {{ $t("status") }}
                    <template v-if="sortColumn === 'active'">
                      <IconC
                        iconName="ArrowLongDownIcon"
                        iconClass="w-4 h-4"
                        v-if="sortDir === 'desc'"
                      />
                      <IconC
                        iconName="ArrowLongUpIcon"
                        iconClass="w-4 h-4"
                        v-else
                      />
                    </template>
                  </div>
                </th>
                <th
                  scope="col"
                  class="py-3 px-6"
                  v-if="$can('execute', 'users')"
                ></th>
              </tr>
            </thead>
            <tbody>
              <template v-for="user in users" :key="user.id">
                <tr
                  class="border-b dark:border-gray-700 bg-white dark:bg-neutral-900 hover:bg-neutral-100/75 dark:hover:bg-neutral-900/[.5]"
                >
                  <th
                    scope="row"
                    class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                  >
                    {{ user.id }}
                  </th>
                  <td class="py-2 px-6">{{ user.firstName }}</td>
                  <td class="py-2 px-6">{{ user.lastName }}</td>
                  <td class="py-2 px-6 max-w-xs">{{ user.username }}</td>
                  <td class="py-2 px-6 max-w-xs">{{ user.email }}</td>
                  <td class="py-2 px-6 max-w-xs">{{ $t(user.userRole) }}</td>
                  <td class="py-2 px-6 max-w-xs">
                    <div
                      class="py-1.5 px-2.5 rounded inline text-white"
                      :class="user.active ? 'bg-green-500' : 'bg-red-500'"
                    >
                      {{ user.active ? $t("active") : $t("inactive") }}
                    </div>
                  </td>
                  <td class="py-2 px-6 w-1.5" v-if="$can('execute', 'users')">
                    <button
                      class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-700"
                      :id="`user-${user.id}-btn`"
                      @click="
                        $toggleDropdown({
                          targetEl: `user-${user.id}-menu`,
                          triggerEl: `user-${user.id}-btn`,
                          placementEl: 'left',
                        })
                      "
                    >
                      <IconC
                        iconName="EllipsisVerticalIcon"
                        iconClass="w-5 h-5 cursor-pointer"
                      />
                    </button>
                    <div
                      :id="`user-${user.id}-menu`"
                      class="hidden z-10 w-32 bg-white rounded shadow-md shadow-gray-400/75 dark:shadow-neutral-700/75 dark:bg-neutral-800"
                      style="inset: 0px auto auto -300px !important"
                    >
                      <ul
                        class="py-1 text-sm font-normal text-gray-700 cursor-pointer divide-y divide-gray-300 dark:divide-gray-700"
                        aria-labelledby="dropdownDefault"
                      >
                        <li
                          class="inline-flex text-theme-700 dark:text-theme-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            $router.push({
                              name: 'user-details',
                              params: { userId: user.id },
                            })
                          "
                        >
                          <IconC
                            iconType="solid"
                            iconName="PencilIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ $t("edit") }}
                        </li>
                        <li
                          class="inline-flex text-red-700 dark:text-red-600 flex-row gap-2 items-center py-2 px-4 hover:bg-neutral-100 dark:hover:bg-neutral-700 w-full"
                          @click="
                            changeUserActiveStatus(
                              JSON.parse(JSON.stringify(user)),
                              !user.active
                            )
                          "
                          v-if="currentUser.id !== user.id"
                        >
                          <IconC
                            iconName="TrashIcon"
                            iconClass="w-5 h-5 cursor-pointer"
                          />
                          {{ user.active ? $t("deactivate") : $t("activate") }}
                        </li>
                      </ul>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
      <red-action-modal
        :actionTitle="selectedUser.active ? $t('activate') : $t('deactivate')"
        :actionText="`${$t('user')}`"
        :isLoading="isDeactivateLoading"
        :modalRef="`deactivate-modal`"
        @submit="deactivateUser()"
      >
      </red-action-modal>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getUsers($event)"
    />
  </div>
</template>

<script>
import RedActionModal from "@/components/modals/RedActionModal.vue";
export default {
  components: {
    RedActionModal,
  },
  data() {
    return {
      isTableLoading: false,
      isDeactivateLoading: false,
      selectedUser: {},
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
      showFilters: false,
    };
  },
  watch: {
    searchQuery: {
      async handler() {
        this.currentPage = 1;
        this.getUsers(1);
      },
    },
    isActiveFilters: {
      async handler() {
        this.currentPage = 1;
        this.getUsers(1);
      },
    },
  },
  computed: {
    users() {
      return this.$store.getters["userModule/getUsersList"];
    },
    pagination() {
      return this.$store.getters["userModule/getUsersPagination"];
    },
    currentUser() {
      return this.$store.state.userModule.currentUser;
    },
    isActiveFilters: {
      get() {
        return this.$store.state.userModule.isActiveFilters;
      },
      set(v) {
        this.$store.state.userModule.isActiveFilters = v;
      },
    },
  },
  created() {
    this.getUsers(this.currentPage);
  },
  methods: {
    changeUserActiveStatus(user, activeStatus) {
      user.active = activeStatus;
      this.selectedUser = user;
      this.$openModal("deactivate-modal");
      this.$putOnFocus("deactivate-item-modal-btn");
    },
    deactivateUser() {
      this.isDeactivateLoading = true;
      this.$store
        .dispatch("userModule/updateUserDetails", this.selectedUser)
        .then(() => {
          this.isDeactivateLoading = false;
          this.getUsers(this.currentPage);
          this.$hideModal("deactivate-modal");
          this.$toast.success(
            this.selectedUser.active
              ? this.$t("activateSuccess", { subject: this.$t("user") })
              : this.$t("deactivateSuccess", { subject: this.$t("user") })
          );
        })
        .catch((error) => {
          this.isDeactivateLoading = false;
          this.$toast.error(error.response.data || this.$t("somethingWrong"));
        });
    },
    getUsers(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("userModule/getUsers", {
          page: page,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
          active: this.isActiveFilters,
        })
        .then(() => {
          this.isTableLoading = false;
          this.currentPage = page;
        })
        .catch(() => {
          this.isTableLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    sort(col) {
      this.sortColumn = col;
      this.sortDir = this.sortDir === "desc" ? "asc" : "desc";
      this.getUsers(this.currentPage);
    },
  },
};
</script>
