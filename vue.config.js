const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        win: {
          icon: "./icon.svg",
        },
        extraResources: [{ from: "./resources/dist/app", to: "./" }],
      },
    },
  },
});
