/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eff6ff",
          500: "#0284c7",
          600: "#0369a1",
          900: "#0c4a6e",
        }
      }
    },
  },
  plugins: [],
};