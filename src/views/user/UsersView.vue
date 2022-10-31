<!-- eslint-disable no-undef -->
<template>
  <div class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4">
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
            class="default-input w-full pl-10"
            :placeholder="$t('search')"
          />
        </div>
      </div>
      <button
        v-if="currentUser.userType === 'admin'"
        @click="
          $router.push({
            name: 'new-user',
          })
        "
        class="blue-gradient-btn flex items-center text-center"
      >
        <IconC iconName="PlusIcon" iconClass="w-5 h-5 mr-2" />
        {{ $t("createNewUser") }}
      </button>
    </div>

    <div class="overflow-hidden rounded-xl my-5 min-h-65 relative">
      <div class="overflow-x-auto overflow-y-hidden scrollbar-style">
        <table
          class="w-full text-sm text-left text-gray-700 dark:text-gray-400"
        >
          <OverlayC v-if="isTableLoading" />
          <EmptyResultsC
            v-if="users.length === 0 && !isTableLoading"
            pluralText="Users"
            singularText="User"
            :search="searchQuery"
            routeName="new-user"
          />
          <thead
            class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400"
          >
            <tr>
              <th
                scope="col"
                class="py-3 px-6"
                v-if="currentUser.userType !== 'staff'"
              ></th>
              <th scope="col" class="py-3 px-6">{{ $t("image") }}</th>
              <th
                scope="col"
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
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
                class="py-3 px-6 hover:bg-gray-200/[.6] hover:dark:bg-gray-600"
                @click="sort('user_type')"
              >
                <div class="flex justify-between items-center">
                  {{ $t("type") }}
                  <template v-if="sortColumn === 'user_type'">
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
              <th scope="col" class="py-3 px-6"></th>
              <th
                scope="col"
                class="py-3 px-6"
                v-if="currentUser.userType !== 'staff'"
              ></th>
            </tr>
          </thead>
          <tbody>
            <template v-for="user in users" :key="user.id">
              <tr
                class="bg-white border-b dark:bg-gray-900 dark:border-gray-700 hover:dark:bg-gray-900/75"
                :class="
                  selectedUser === user
                    ? 'bg-blue-100 dark:bg-blue-800/25 hover:dark:bg-blue-800/25'
                    : ''
                "
              >
                <td
                  class="py-2 px-6"
                  @click="updateSelectedUser(user)"
                  v-if="currentUser.userType !== 'staff'"
                >
                  <template v-if="currentUser.id !== user.id">
                    <IconC
                      v-if="selectedUser === user"
                      iconName="CheckCircleIcon"
                      iconClass="h-5 w-5 fill-blue-500 text-gray-900 dark:text-gray-300 dark:fill-blue-700"
                    />
                    <IconC
                      v-else
                      iconName="MinusCircleIcon"
                      iconClass="h-5 w-5 text-gray-900 dark:text-gray-300"
                    />
                  </template>
                </td>
                <th
                  scope="row"
                  class="py-2 px-6 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <img
                    class="w-7 h-7 rounded-full border-2 border-gray-500"
                    src="http://localhost:5000/static/profile-2.png"
                    alt="user photo"
                  />
                </th>
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
                <td class="py-2 px-6 max-w-xs">{{ user.userType }}</td>
                <td
                  class="py-2 px-6"
                  @click="
                    $router.push({
                      name: 'user-details',
                      params: { userId: user.id },
                    })
                  "
                >
                  <button
                    class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                  >
                    <IconC
                      iconType="solid"
                      iconName="PencilIcon"
                      iconClass="w-5 h-5 text-blue-700 cursor-pointer"
                    />
                  </button>
                </td>
                <td class="py-2 px-6" v-if="currentUser.userType !== 'staff'">
                  <button
                    class="p-1.5 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800"
                    @click="deleteUser(user)"
                    v-if="currentUser.id !== user.id"
                  >
                    <IconC
                      iconName="TrashIcon"
                      iconClass="w-5 h-5 text-red-700 cursor-pointer"
                    />
                  </button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
    <PaginationC
      :pagination="pagination"
      :currentPage="currentPage"
      @pageChange="getUsers($event)"
    />
    <delete-modal
      :productId="selectedUserToDelete.id"
      deleteAction="userModule/deleteUser"
      getAction="userModule/getUsers"
      title="User"
      deleteRef="delete-modal"
      @reload="getUsers(currentPage)"
    >
    </delete-modal>
  </div>
</template>

<script>
import DeleteModal from "@/components/modals/DeleteModal.vue";
export default {
  components: {
    DeleteModal,
  },
  data() {
    return {
      isTableLoading: false,
      selectedUser: {},
      selectedUserToDelete: {},
      currentPage: 1,
      searchQuery: "",
      sortColumn: null,
      sortDir: "desc",
    };
  },
  watch: {
    searchQuery: {
      async handler(value) {
        this.isTableLoading = true;
        this.currentPage = 1;
        try {
          await this.$store.dispatch("userModule/getUsers", {
            page: this.currentPage,
            search: value,
            sort_column: this.sortColumn,
            sort_dir: this.sortDir,
          });
          this.isTableLoading = false;
        } catch {
          this.isTableLoading = false;
        }
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
  },
  created() {
    window.addEventListener("keydown", (e) => {
      if (e.key == "Delete") {
        const isEmpty = Object.keys(this.selectedUser).length === 0;
        if (!isEmpty) {
          this.deleteUser(this.selectedUser);
        }
      }
    });
    this.getUsers(this.currentPage);
  },
  methods: {
    updateSelectedUser(user) {
      if (this.selectedUser.id === user.id) {
        this.selectedUser = {};
      } else {
        this.selectedUser = user;
      }
    },
    deleteUser(user) {
      this.selectedUserToDelete = user;
      this.$openModal("delete-modal");
      this.$putOnFocus("delete-product-modal-btn");
    },
    getUsers(page) {
      this.isTableLoading = true;
      this.$store
        .dispatch("userModule/getUsers", {
          page: page,
          search: this.searchQuery,
          sort_column: this.sortColumn,
          sort_dir: this.sortDir,
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
