<template>
  <section class="bg-neutral-100 dark:bg-neutral-900">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto min-h-screen xl:py-0"
    >
      <div
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        <IconC
          iconType="custom"
          iconName="FlowbiteIcon"
          iconClass="w-9 h-9 mr-2"
        />
        <div>
          <span
            class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
          >
            Egzoni
          </span>
          <span
            class="text-sm font-semibold whitespace-nowrap dark:text-gray-300"
          >
            Market
          </span>
        </div>
      </div>
      <div
        class="w-full bg-white rounded shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-neutral-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            Sign up / Create account
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
                rules="required"
                type="email"
                name="email"
                id="email"
                :class="errors.email ? 'ring-2 ring-red-500' : ''"
                class="bg-neutral-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
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
                rules="required"
                type="text"
                name="firstName"
                id="firstName"
                :class="errors.firstName ? 'ring-2 ring-red-500' : ''"
                class="bg-neutral-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
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
                rules="required"
                type="text"
                name="lastName"
                id="lastName"
                :class="errors.lastName ? 'ring-2 ring-red-500' : ''"
                class="bg-neutral-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
                placeholder="Doe"
                required=""
              />
              <span class="text-red-700">{{ errors.lastName }}</span>
            </div>
            <div>
              <label
                for="username"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your Username</label
              >
              <Field
                v-model="username"
                rules="required"
                type="text"
                name="username"
                id="username"
                :class="errors.username ? 'ring-2 ring-red-500' : ''"
                class="bg-neutral-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
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
                rules="required"
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                :class="errors.password ? 'ring-2 ring-red-500' : ''"
                class="bg-neutral-50 border border-gray-300 text-gray-900 sm:text-sm rounded focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-neutral-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-theme-500 dark:focus:border-theme-500"
                required=""
              />
              <span class="text-red-700">{{ errors.password }}</span>
            </div>
            <p
              class="text-sm font-light text-gray-500 dark:text-gray-400 flex justify-end gap-1"
            >
              Already have an account?
              <router-link
                :to="{ name: 'signin' }"
                class="font-medium text-theme-600 hover:underline dark:text-theme-500"
                >Sign in</router-link
              >
            </p>
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
              <div v-else>Sign up</div>
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
      isLoading: false,
    };
  },
  mounted() {
    document.getElementById("app").classList.remove("sidebar-opened");
  },
  beforeMount() {
    document.getElementById("app").classList.add("sidebar-opened");
  },
  methods: {
    create() {
      this.isLoading = true;
      const data = {
        email: this.email,
        password: this.password,
        firstName: this.firstName,
        lastName: this.lastName,
        username: this.username,
        userRole: null,
      };
      this.$store
        .dispatch("userModule/createUser", data)
        .then(() => {
          this.$router.push({ name: "signin" });
          this.$toast.success("You have successfully signed up!");
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
</style>
