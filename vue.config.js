const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  pluginOptions: {
    electronBuilder: {
      builderOptions: {
        win: {
          icon: "./src/assets/images/icon.svg",
        },
        extraResources: [{ from: "./resources/dist/app", to: "./" }],
        productName: "Egzoni Market",
      },
    },
  },
});
