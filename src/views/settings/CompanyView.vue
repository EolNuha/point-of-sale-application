<template>
  <div class="main-div">
    <p class="text-4xl text-center text-gray-700 dark:text-gray-200">
      {{ $t("companyInfo") }}
    </p>
    <div
      class="w-full my-auto mt-5 rounded bg-white dark:bg-neutral-900 p-6 sm:p-8 flex flex-col grow relative"
    >
      <OverlayC
        v-if="isDataLoading"
        outer-div="opacity-100 bg-neutral-100 dark:bg-neutral-900 "
      />
      <Form
        v-slot="{ errors }"
        class="space-y-4 md:space-y-6 mt-5"
        @submit="update"
      >
        <div class="grid grid-cols-2 gap-[20px]">
          <div>
            <label
              for="companyName"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >{{ $t("name") }}</label
            >
            <Field
              v-model="company.name"
              type="text"
              name="companyName"
              id="companyName"
              :class="errors.companyName ? 'ring-2 ring-red-500' : ''"
              class="default-input w-full"
              :placeholder="$t('name')"
            />
            <span class="text-red-700">{{ errors.companyName }}</span>
          </div>
          <div>
            <label
              for="address"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >{{ $t("address") }}</label
            >
            <Field
              v-model="company.address"
              type="text"
              name="address"
              id="address"
              :class="errors.address ? 'ring-2 ring-red-500' : ''"
              class="default-input w-full"
              :placeholder="$t('address')"
            />
            <span class="text-red-700">{{ errors.address }}</span>
          </div>
          <div>
            <label
              for="phoneNumber"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >{{ $t("phone") }}</label
            >
            <Field
              v-model="company.phone"
              rules="phonexk"
              type="text"
              name="phoneNumber"
              id="phoneNumber"
              :class="errors.phoneNumber ? 'ring-2 ring-red-500' : ''"
              class="default-input w-full"
              :placeholder="$t('phone')"
            />
            <span class="text-red-700">{{ errors.phoneNumber }}</span>
          </div>
          <div>
            <label
              for="taxNumber"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >{{ $t("tax_number") }}</label
            >
            <Field
              v-model="company.tax_number"
              type="number"
              name="taxNumber"
              id="taxNumber"
              :class="errors.taxNumber ? 'ring-2 ring-red-500' : ''"
              class="default-input w-full"
              :placeholder="$t('tax_number')"
            />
            <span class="text-red-700">{{ errors.taxNumber }}</span>
          </div>
          <div>
            <label
              for="fiscalNumber"
              class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >{{ $t("fiscal_number") }}</label
            >
            <Field
              v-model="company.fiscal_number"
              type="number"
              name="fiscalNumber"
              id="fiscalNumber"
              :class="errors.fiscalNumber ? 'ring-2 ring-red-500' : ''"
              class="default-input w-full"
              :placeholder="$t('fiscal_number')"
            />
            <span class="text-red-700">{{ errors.fiscalNumber }}</span>
          </div>
        </div>
        <div class="hidden">
          <label
            for="logo"
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white none"
            >{{ $t("logo") }}</label
          >
          <input
            @input="onImageInput"
            ref="companyImage"
            type="file"
            name="logo"
            id="logo"
            :class="errors.logo ? 'ring-2 ring-red-500' : ''"
            class="default-input w-full"
            placeholder="Company Name"
            accept="image/*"
          />
          <span class="text-red-700">{{ errors.logo }}</span>
        </div>
        <div>
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white none"
            >{{ $t("logo") }}</label
          >
          <div
            @click="$refs.companyImage.click()"
            class="w-[150px] h-[150px] bg-neutral-200 dark:bg-neutral-800 rounded flex items-center justify-center text-center cursor-pointer relative m-0"
          >
            <p v-if="!company.logo" class="text-gray-700 dark:text-gray-200">
              {{ $t("clickToUpload") }}
            </p>
            <img v-else :src="company.logo" class="max-w-[100%] max-h-[100%]" />
            <button
              v-if="company.logo"
              class="x-btn bg-neutral-300 dark:bg-neutral-800"
              @click.stop="clearImage"
              type="button"
            >
              <IconC
                iconName="XMarkIcon"
                iconClass="w-5 h-5 text-gray-700 dark:text-gray-200"
              />
            </button>
          </div>
        </div>
        <button
          type="submit"
          class="min-w-[100px] theme-gradient-btn flex justify-center items-center"
          :disabled="isLoading"
        >
          <div role="status" v-if="isLoading">
            <IconC
              iconType="custom"
              iconName="SpinnerIcon"
              iconClass="w-4 h-4 text-gray-200 animate-spin fill-theme-600"
            />
            <span class="sr-only">Loading...</span>
          </div>
          <div v-else>{{ $t("update") }}</div>
        </button>
      </Form>
    </div>
  </div>
</template>

<script>
import { Field, Form } from "vee-validate";
import JsonToFormData from "@/services/mixins/JsonToFormData";
import { defineRule } from "vee-validate";
export default {
  components: { Field, Form },
  mixins: [JsonToFormData],
  data() {
    return {
      isLoading: false,
      isDataLoading: true,
    };
  },
  beforeCreate() {
    defineRule("phonexk", (value) => {
      if (!value) return true;
      const pattern = /^\+\d{3} ?\d{8}$/;
      if (pattern.test(value)) {
        return true;
      } else {
        return this.$t("phoneMsg");
      }
    });
  },
  async mounted() {
    this.isDataLoading = true;
    await this.$store.dispatch("settingsModule/getCompany");
    this.isDataLoading = false;
  },
  computed: {
    company: {
      get() {
        return this.$store.state.settingsModule.company;
      },
      set(v) {
        this.$store.commit("SET_COMPANY", v);
      },
    },
  },
  methods: {
    async update() {
      this.isLoading = true;
      const f = this.jsonToFormData(this.company);
      await this.$store.dispatch("settingsModule/updateCompany", f).then(() => {
        this.$toast.success(this.$t("companySuccess"));
      });
      this.isLoading = false;
    },
    onImageInput(e) {
      const allowedTypes = ["png", "jpg", "jpeg", "webp", "gif", "svg"];
      const f = e.target.files[0];
      const { type } = f;
      if (!allowedTypes.includes(type.split("/")[1])) {
        this.$refs.companyImage.value = null;
        this.$toast.warning(this.$t("imageTypesError"));
        return;
      }
      if (f) {
        this.company.logo = URL.createObjectURL(f);
        this.company.file = f;
      }
    },
    clearImage() {
      this.company.logo = null;
      this.company.file = null;
      this.$refs.companyImage.value = null;
    },
  },
};
</script>

<style lang="scss" scoped>
.x-btn {
  position: absolute;
  outline: none;
  border: 0;
  top: 0;
  right: 0;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transform: translate(25%, -25%);
}
</style>
