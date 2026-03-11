/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#17201c",
        moss: "#4b7a5a",
        soil: "#815738",
        sand: "#f0e5d0",
        leaf: "#d3e8c8",
      },
      fontFamily: {
        sans: ["'IBM Plex Sans KR'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
