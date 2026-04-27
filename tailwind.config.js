/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./donations/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4a6fa5',
        soft: '#f5f7fa',
      },
    },
  },
  plugins: [],
}