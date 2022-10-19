<template>
  <div
    class="flex-col flex bg-gray-200 dark:bg-gray-800 min-h-screen p-4 relative"
  >
    <div
      class="w-full md:w-[70%] md:mx-auto my-auto px-4 rounded-xl bg-white dark:bg-gray-900 px-5 py-10 sm:px-20 relative"
    >
      <OverlayC v-if="isDataLoading" />
      <div class="flex items-center justify-center gap-4">
        <img
          class="w-24 h-24 rounded-full border-4 border-gray-500"
          src="http://localhost:5000/static/profile-2.png"
          alt="user photo"
        />
        <h2
          class="capitalize font-extrabold text-2xl md:text-4xl text-gray-700 dark:text-gray-300"
        >
          {{ user.firstName }} {{ user.lastName }}
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
            :rules="isRequired"
            type="email"
            name="email"
            id="email"
            :class="errors.email ? 'ring-2 ring-red-500' : ''"
            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="name@company.com"
            required
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.email }}</span>
        </div>
        <div>
          <label
            for="firstName"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("firstName") }}</label
          >
          <Field
            v-model="user.firstName"
            :rules="isRequired"
            type="text"
            name="firstName"
            id="firstName"
            :class="errors.firstName ? 'ring-2 ring-red-500' : ''"
            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="John"
            required=""
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.firstName }}</span>
        </div>
        <div>
          <label
            for="lastName"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("lastName") }}</label
          >
          <Field
            v-model="user.lastName"
            :rules="isRequired"
            type="text"
            name="lastName"
            id="lastName"
            :class="errors.lastName ? 'ring-2 ring-red-500' : ''"
            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Doe"
            required=""
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.lastName }}</span>
        </div>
        <div>
          <label
            for="username"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("username") }}</label
          >
          <Field
            v-model="user.username"
            :rules="isRequired"
            type="text"
            name="username"
            id="username"
            :class="errors.username ? 'ring-2 ring-red-500' : ''"
            class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="johndoe"
            required
            :disabled="isDisabled()"
          />
          <span class="text-red-700">{{ errors.username }}</span>
        </div>
        <div>
          <label
            for="userType"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{{ $t("userType") }}</label
          >
          <v-select
            class="block w-full default-input !p-1"
            v-model="user.userType"
            :clearable="false"
            :options="['staff', 'admin']"
            type="text"
            name="userType"
            id="userType"
            placeholder="User Type"
            :disabled="isDisabled()"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full blue-gradient-btn flex justify-center items-center"
          :disabled="isLoading || isDisabled()"
        >
          <div role="status" v-if="isLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-blue-600"
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
      })
      .catch(() => {
        this.isDataLoading = false;
      });
  },
  methods: {
    isRequired(value) {
      return value ? true : this.$t("isRequired");
    },
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
        this.currentUser.userType === "admin" ||
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
