<template>
  <section class="bg-gray-100 dark:bg-gray-900">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto min-h-screen lg:py-0"
    >
      <div
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        <img
          class="w-8 h-8 mr-2"
          src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg"
          alt="logo"
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
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            Sign in to your account
          </h1>
          <Form
            v-slot="{ errors }"
            class="space-y-4 md:space-y-6"
            @submit="signin"
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
                required
              />
              <span class="text-red-700">{{ errors.password }}</span>
            </div>
            <div class="flex justify-end items-center">
              <router-link
                :to="{ name: 'signup' }"
                class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500"
                >Forgot password?</router-link
              >
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
              <div v-else>Sign in</div>
            </button>
            <p class="text-sm font-light text-gray-500 dark:text-gray-400">
              Don’t have an account yet?
              <router-link
                :to="{ name: 'signup' }"
                class="font-medium text-blue-600 hover:underline dark:text-blue-500"
                >Sign up</router-link
              >
            </p>
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
    isRequired(value) {
      return value ? true : "This field is required";
    },
    signin() {
      this.isLoading = true;
      const data = {
        email: this.email,
        password: this.password,
      };
      this.$store
        .dispatch("userModule/signinUser", data)
        .then((res) => {
          localStorage.removeItem("token");
          localStorage.setItem("token", res.data.token);
          this.$store.dispatch("userModule/getCurrentUser");
          this.$router.push({
            name: "dashboard",
          });
          this.$toast.success("You have successfully signed in!");
        })
        .catch((err) => {
          this.$toast.error(err.response.data);
          this.isLoading = false;
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
