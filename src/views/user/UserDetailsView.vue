<template>
  <div class="main-div relative">
    <div
      class="w-full sm:max-w-md md:mx-auto my-auto rounded bg-white dark:bg-neutral-900 p-6 sm:p-8 flex flex-col grow relative"
    >
      <OverlayC v-if="isDataLoading" />
      <div class="flex items-center justify-center">
        <h2
          class="capitalize font-extrabold text-2xl md:text-4xl text-gray-700 dark:text-gray-300"
        >
          {{ user.first_name }} {{ user.last_name }}
        </h2>
      </div>
      <Form
        v-slot="{ errors }"
        class="space-y-4 md:space-y-6 mt-5"
        @submit="update"
      >
        <div>
          <label
            for="email"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("email") }}</label
          >
          <Field
            v-model="user.email"
            rules="required"
            type="email"
            name="email"
            id="email"
            :class="errors.email ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="name@company.com"
            required
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.email }}</span>
        </div>
        <div>
          <label
            for="first_name"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("first_name") }}</label
          >
          <Field
            v-model="user.first_name"
            rules="required"
            type="text"
            name="first_name"
            id="first_name"
            :class="errors.first_name ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="John"
            required=""
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.first_name }}</span>
        </div>
        <div>
          <label
            for="last_name"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("last_name") }}</label
          >
          <Field
            v-model="user.last_name"
            rules="required"
            type="text"
            name="last_name"
            id="last_name"
            :class="errors.last_name ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Doe"
            required=""
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.last_name }}</span>
        </div>
        <div>
          <label
            for="username"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("username") }}</label
          >
          <Field
            v-model="user.username"
            rules="required"
            type="text"
            name="username"
            id="username"
            :class="errors.username ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="johndoe"
            required
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.username }}</span>
        </div>
        <div>
          <label
            for="user_role"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("user_role") }}</label
          >
          <v-select
            class="block w-full default-input !p-1"
            v-model="user.user_role"
            :clearable="false"
            :options="
              currentUser.user_role === 'superadmin'
                ? ['staff', 'manager', 'owner', 'superadmin']
                : ['staff', 'manager', 'owner']
            "
            type="text"
            name="user_role"
            id="user_role"
            :placeholder="$t('user_role')"
            :disabled="isDisabled() || !$can('execute', 'users')"
            required
            label="option"
          >
            <template #selected-option="{ option }">
              {{ $t(option) }}
            </template>
            <template #option="{ option }">
              {{ $t(option) }}
            </template>
          </v-select>
        </div>
        <button
          type="submit"
          class="w-full theme-gradient-btn flex justify-center items-center"
          :disabled="isLoading || isDisabled()"
        >
          <div role="status" v-if="isLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
            />
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else>Submit</div>
        </button>
      </Form>
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
      isLoading: false,
      isDataLoading: true,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.userModule.currentUser;
    },
    user() {
      return this.$store.state.userModule.user;
    },
  },
  created() {
    this.$store
      .dispatch("userModule/getUserDetails", this.$route.params.userId)
      .then(() => {
        this.isDataLoading = false;
        document.title = `${this.user.first_name} ${this.user.last_name}`;
      })
      .catch(() => {
        this.isDataLoading = false;
      });
  },
  methods: {
    update() {
      this.isLoading = true;
      this.$store
        .dispatch("userModule/updateUserDetails", this.user)
        .then(() => {
          this.isLoading = false;
          this.$toast.success(this.$t("userUpdateSuccess"));
          this.$store.dispatch("userModule/getCurrentUser");
        })
        .catch(() => {
          this.isLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
        });
    },
    isDisabled() {
      if (
        this.$can("execute", "users") ||
        this.currentUser.id === this.user.id
      ) {
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>
