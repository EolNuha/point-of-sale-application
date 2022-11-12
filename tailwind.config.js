const colors = require("tailwindcss/colors");
module.exports = {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "node_modules/flowbite/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        theme: {
          50: "var(--color-theme-50)",
          100: "var(--color-theme-100)",
          200: "var(--color-theme-200)",
          300: "var(--color-theme-300)",
          400: "var(--color-theme-400)",
          500: "var(--color-theme-500)",
          600: "var(--color-theme-600)",
          700: "var(--color-theme-700)",
          800: "var(--color-theme-800)",
          900: "var(--color-theme-900)",
        },
        ...colors,
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
