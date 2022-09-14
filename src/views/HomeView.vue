<template>
  <div class="justify-center flex-col flex bg-gray-300 items-center h-screen">
    <div class="text-5xl">First Desktop App</div>
    <button @click="test">click me</button>
    <p>{{ $store.state.something }}</p>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "HomeView",
  created() {
    this.$store.dispatch("getSomething");
  },
  methods: {
    test() {
      this.$store.dispatch("getSomething");
    },
  },
};
</script>
