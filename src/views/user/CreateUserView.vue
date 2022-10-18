<template>
  <section class="bg-gray-100 dark:bg-gray-800">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto min-h-screen"
    >
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-900 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            Create user account
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
                >Your email</label
              >
              <Field
                v-model="email"
                :rules="isRequired"
                type="email"
                name="email"
                id="email"
                :class="errors.email ? 'ring-2 ring-red-500' : ''"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="name@company.com"
                required
              />
              <span class="text-red-700">{{ errors.email }}</span>
            </div>
            <div>
              <label
                for="firstName"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your First Name</label
              >
              <Field
                v-model="firstName"
                :rules="isRequired"
                type="text"
                name="firstName"
                id="firstName"
                :class="errors.firstName ? 'ring-2 ring-red-500' : ''"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="John"
                required=""
              />
              <span class="text-red-700">{{ errors.firstName }}</span>
            </div>
            <div>
              <label
                for="lastName"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your Last Name</label
              >
              <Field
                v-model="lastName"
                :rules="isRequired"
                type="text"
                name="lastName"
                id="lastName"
                :class="errors.lastName ? 'ring-2 ring-red-500' : ''"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Doe"
                required=""
              />
              <span class="text-red-700">{{ errors.lastName }}</span>
            </div>
            <div>
              <label
                for="lastName"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >User Type</label
              >
              <v-select
                class="block w-full default-input !p-1"
                v-model="userType"
                :clearable="false"
                :options="['staff', 'admin']"
                type="text"
                name="userType"
                id="userType"
                placeholder="User Type"
                required
              />
            </div>
            <div>
              <label
                for="username"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your Username</label
              >
              <Field
                v-model="username"
                :rules="isRequired"
                type="text"
                name="username"
                id="username"
                :class="errors.username ? 'ring-2 ring-red-500' : ''"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="johndoe"
                required
              />
              <span class="text-red-700">{{ errors.username }}</span>
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Password</label
              >
              <Field
                v-model="password"
                :rules="isRequired"
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                :class="errors.password ? 'ring-2 ring-red-500' : ''"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required=""
              />
              <span class="text-red-700">{{ errors.password }}</span>
            </div>
            <button
              type="submit"
              class="w-full blue-gradient-btn flex justify-center items-center"
              :disabled="isLoading"
            >
              <div role="status" v-if="isLoading">
                <IconC
                  iconType="custom"
                  iconName="SpinnerIcon"
                  iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
                />
                <span class="sr-only">Loading...</span>
              </div>
              <div v-else>Create User</div>
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
      firstName: "",
      lastName: "",
      username: "",
      userType: "staff",
      isLoading: false,
    };
  },
  methods: {
    isRequired(value) {
      return value ? true : "This field is required";
    },
    create() {
      this.isLoading = true;
      const data = {
        email: this.email,
        password: this.password,
        firstName: this.firstName,
        lastName: this.lastName,
        username: this.username,
        userType: this.userType,
      };
      this.$store
        .dispatch("userModule/createUser", data)
        .then(() => {
          this.$router.push({ name: "users" });
          this.$toast.success("You have successfully created an account!");
        })
        .catch(() => {
          this.isLoading = false;
          this.$toast.error(this.$t("somethingWrong"));
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
