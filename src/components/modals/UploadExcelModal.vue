<template>
  <div
    :id="modalRef"
    :ref="modalRef"
    tabindex="-1"
    class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 md:inset-0 h-modal md:h-full"
  >
    <div class="relative p-4 w-full max-w-3xl h-full md:h-auto">
      <div class="relative bg-white rounded shadow dark:bg-neutral-700">
        <div
          class="text-gray-700 dark:text-gray-200 flex justify-between items-center p-2.5"
        >
          <p class="text-xl">{{ $t("upload") }} Excel</p>
          <button
            type="button"
            class="p-2.5 rounded-full hover:bg-neutral-300/50 dark:hover:bg-neutral-800/50"
            @click="$hideModal(modalRef)"
            :disabled="isLoading"
          >
            <IconC iconName="XMarkIcon" iconClass="w-5 h-5" />
          </button>
        </div>
        <div class="p-6">
          <label
            class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            for="file_input"
            >{{ $t("upload") }} file</label
          >
          <input
            ref="excelFile"
            @input="onFileInput"
            class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            id="file_input"
            type="file"
          />
          <div
            class="bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-200 rounded-md p-2 mt-5"
          >
            {{ $t("excelTemplateDownloadDescription") }}
            <a
              class="underline text-theme-500"
              href="http://localhost:5000/static/EXCEL_TEMPLATE.xlsx"
              download="EXCEL_TEMPLATE"
              >{{ $t("here") }}</a
            >.
            <br />
            <ul
              role="list"
              class="flex flex-col gap-2 list-decimal list-inside"
            >
              <li>{{ $t("taxRules") }}</li>
              <li>{{ $t("purchasePriceRules") }}</li>
              <li>{{ $t("measureRules") }}</li>
            </ul>
          </div>
          <div class="flex items-center justify-end gap-2 mt-6">
            <button
              @click="$hideModal(modalRef)"
              :disabled="isLoading"
              type="button"
              class="gray-outline-btn h-10 w-20 inline-flex items-center justify-center"
            >
              {{ $t("cancel") }}
            </button>
            <button
              @click="submit"
              :id="modalRef + '_remove_btn'"
              :ref="modalRef + '_remove_btn'"
              type="button"
              class="theme-gradient-btn h-10 w-20 inline-flex justify-center items-center"
            >
              <IconC
                v-if="isLoading"
                iconType="custom"
                iconName="SpinnerIcon"
                iconClass="mr-2 w-4 h-4 text-gray-200 animate-spin fill-red-600"
              />
              <span v-else>{{ $t("upload") }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modalRef: { type: String, required: true, default: "excel-upload-modal" },
    icon: {
      type: Object,
      required: false,
      default: () => ({
        name: "ExclamationCircleIcon",
        class: "mx-auto mb-4 w-14 h-14 text-gray-400 dark:text-gray-200",
      }),
    },
  },
  data() {
    return {
      isLoading: false,
    };
  },
  methods: {
    onFileInput(e) {
      const allowedTypes = [
        "xlsx",
        "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      ];
      const f = e.target.files[0];
      const { type } = f;
      console.log(type);
      if (!allowedTypes.includes(type.split("/")[1])) {
        this.$refs.excelFile.value = null;
        this.$toast.warning(this.$t("imageTypesError"));
        return;
      }
      if (f) {
        this.file = f;
      }
    },
    async submit() {
      console.log(this.file);
      this.isLoading = true;
      const fd = new FormData();
      fd.append("file", this.file);
      await this.$store
        .dispatch("productModule/uploadProductsExcel", fd)
        .then(() => {
          this.$hideModal(this.modalRef);
          this.$emit("reload");
        });
      this.isLoading = false;
    },
  },
};
</script>
