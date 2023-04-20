<template>
  <section class="bg-neutral-100 dark:bg-neutral-900">
    <div
      class="flex flex-col items-center justify-center px-6 py-8 mx-auto min-h-screen lg:py-0"
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
            {{ $t("signinToAccount") }}
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
                >{{ $t("email") }} / {{ $t("username") }}</label
              >
              <Field
                v-model="email"
                rules="required"
                type="text"
                name="email"
                id="email"
                :class="errors.email ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                :placeholder="$t('enterEmailOrUsername')"
                required
              />
              <span class="text-red-700">{{ errors.email }}</span>
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
                :placeholder="$t('enterPassword')"
                :class="errors.password ? 'ring-2 ring-red-500' : ''"
                class="default-input w-full"
                required
              />
              <span class="text-red-700">{{ errors.password }}</span>
            </div>
            <!-- <div class="flex justify-end items-center">
              <router-link
                :to="{ name: 'signup' }"
                class="text-sm font-medium text-theme-600 hover:underline dark:text-theme-500"
                >Forgot password?</router-link
              >
            </div> -->
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
              <div v-else>{{ $t("signin") }}</div>
            </button>
            <!-- <p class="text-sm font-light text-gray-500 dark:text-gray-400">
              Don’t have an account yet?
              <router-link
                :to="{ name: 'signup' }"
                class="font-medium text-theme-600 hover:underline dark:text-theme-500"
                >Sign up</router-link
              >
            </p> -->
          </Form>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import { Field, Form } from "vee-validate";
import UserData from "@/services/mixins/UserData";
export default {
  components: {
    Field,
    Form,
  },
  mixins: [UserData],
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
    signin() {
      this.isLoading = true;
      const data = {
        email: this.email,
        password: this.password,
      };
      this.$store
        .dispatch("userModule/signinUser", data)
        .then(async (res) => {
          localStorage.removeItem("token");
          localStorage.setItem("token", res.data.token);
          await this.$store.dispatch("userModule/getCurrentUser");
          this.setUserData();
          this.$router.push({
            name: "dashboard",
          });
          this.$toast.success(this.$t("signinSuccess"));
        })
        .catch((err) => {
          this.$toast.error(this.$t(err.response.data));
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
