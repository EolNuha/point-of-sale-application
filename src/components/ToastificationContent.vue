<template>
  <div class="toastification" :class="variant">
    <div class="d-flex align-items-center">
      <!-- <GjIcon :name="icon" size="2rem" :color="color" /> -->
      <!-- <b-avatar
        :variant="variant"
        class="mr-75 flex-shrink-0"
      > -->
      <!-- <feather-icon
          :icon="icon"
          size="15"
        /> -->
      <!-- </b-avatar> -->
      <div class="d-flex flex-grow-1 ml-05">
        <div>
          <!-- <h5
            v-if="title"
            class="mb-0 font-weight-bolder toastification-title"
            :class="`text-${variant}`"
            v-text="title"
          /> -->
          <div
            v-if="text"
            class="d-inline-block text-body text-primary text-main text-xsm"
            v-text="text"
          />
        </div>
        <span
          class="cursor-pointer toastification-close-icon ml-auto"
          @click="$emit('close-toast')"
        >
          <GjIcon v-if="!hideClose" name="Close" color="#333" />
        </span>
      </div>
    </div>
  </div>
</template>

<script>
// import { BAvatar } from 'bootstrap-vue'

export default {
  components: {
    // BAvatar,
  },
  props: {
    variant: {
      type: String,
      default: "primary",
    },
    icon: {
      type: String,
      default: null,
    },
    title: {
      type: String,
      default: null,
    },
    text: {
      type: String,
      default: null,
    },
    hideClose: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    color() {
      switch (this.variant) {
        case "success":
          return "#36B37E";
        case "danger":
          return "#E34850";
        case "warn":
          return "#FFCC00";
        default:
          return "#3A81F6";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.toastification-close-icon,
.toastification-title {
  line-height: 26px;
}

.toastification-title {
  color: inherit;
}

.text-body {
  word-break: break-word;
}
</style>

<style lang="scss" scoped>
.toastification {
  &:after {
    content: "";
    position: absolute;
    width: 5px;
    height: 100%;
    left: 0px;
    border-radius: 4px 0px 0px 4px;
    top: 0;
  }

  &.success {
    &::after {
      background: green;
    }
  }

  &.danger {
    &::after {
      background: red;
    }
  }

  &.warn {
    &::after {
      background: yellow;
    }
  }
  &.primary {
    &::after {
      background: blue;
    }
  }
}
</style>
