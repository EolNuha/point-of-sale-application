<template>
  <div
    class="bg-neutral-200 dark:bg-neutral-800 min-h-screen p-3 flex items-center justify-center flex-col"
  >
    <img src="@/assets/images/404.svg" class="max-w-full w-[30rem]" />
    <h1 class="text-gray-700 dark:text-gray-300 text-6xl font-extrabold">
      Page not found
    </h1>
    <p class="text-gray-500 my-3">
      Oops! Looks like you followed a bad link. If you think this is a problem
      with us, please tell us.
    </p>
    <button
      class="theme-gradient-btn flex items-center"
      @click="
        $router.push({
          name: 'dashboard',
        })
      "
    >
      <IconC iconName="HomeIcon" iconClass="w-5 h-5 mr-2" />Go back home
    </button>
  </div>
</template>

<script>
export default {};
</script>
