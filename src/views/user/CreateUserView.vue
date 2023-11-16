<template>
  <section class="bg-neutral-100 dark:bg-neutral-800">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto min-h-screen"
    >
      <div
        class="w-full bg-white rounded shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-neutral-900 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            {{ $t("createUserAccount") }}
          </h1>
          <Form
            v-slot="{ errors }"
            class="space-y-4 md:space-y-6"
            @submit="create"
          >
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >{{ $t("email") }}</label
              >
              <Field
                v-model="email"
                rules="required"
                type="email"
                name="email"
                id="email"
                :class="errors.email ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                placeholder="name@company.com"
                required
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
                v-model="first_name"
                rules="required"
                type="text"
                name="first_name"
                id="first_name"
                :class="errors.first_name ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                placeholder="John"
                required=""
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
                v-model="last_name"
                rules="required"
                type="text"
                name="last_name"
                id="last_name"
                :class="errors.last_name ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                placeholder="Doe"
                required=""
              />
              <span class="text-red-700">{{ errors.last_name }}</span>
            </div>
            <div>
              <label
                for="user_role"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >{{ $t("user_role") }}</label
              >
              <v-select
                class="block w-full default-input !p-1"
                v-model="user_role"
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
            <div>
              <label
                for="username"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >{{ $t("username") }}</label
              >
              <Field
                v-model="username"
                rules="required"
                type="text"
                name="username"
                id="username"
                :class="errors.username ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                placeholder="johndoe"
                required
              />
              <span class="text-red-700">{{ errors.username }}</span>
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >{{ $t("password") }}</label
              >
              <Field
                v-model="password"
                rules="required"
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                :class="errors.password ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                required=""
              />
              <span class="text-red-700">{{ errors.password }}</span>
            </div>
            <button
              type="submit"
              class="w-full theme-gradient-btn flex justify-center items-center"
              :disabled="isLoading"
            >
              <div role="status" v-if="isLoading">
                <IconC
                  iconType="custom"
                  iconName="SpinnerIcon"
                  iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-theme-600"
                />
                <span class="sr-only">Loading...</span>
              </div>
              <div v-else>{{ $t("createUser") }}</div>
            </button>
          </Form>
        </div>
      </div>
    </div>
  </section>
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
      email: "",
      password: "",
      first_name: "",
      last_name: "",
      username: "",
      user_role: "staff",
      isLoading: false,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.userModule.currentUser;
    },
  },
  methods: {
    create() {
      this.isLoading = true;
      const data = {
        email: this.email,
        password: this.password,
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.username,
        user_role: this.user_role,
      };
      this.$store
        .dispatch("userModule/createUser", data)
        .then(() => {
          this.$router.push({ name: "users" });
          this.$toast.success(this.$t("successfullyCreatedAccount"));
        })
        .catch((err) => {
          this.isLoading = false;
          this.$toast.error(
            this.$t(err.response.data) || this.$t("somethingWrong")
          );
        });
    },
  },
};
</script>

<style scoped>
.min-h-screen {
  min-height: 100vh !important;
}
.vs__search,
.vs__search:focus {
  padding: 0 !important;
}
</style>
