/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        serif: ["Cormorant Garamond", "Georgia", "serif"],
        sans: ["DM Sans", "system-ui", "sans-serif"],
      },
      colors: {
        black: "#0a0a0a",
        offwhite: "#fafafa",
      },
      letterSpacing: {
        tight: "-0.02em",
        wide: "0.08em",
      },
      borderColor: {
        DEFAULT: "#e5e5e5",
      },
    },
  },
  plugins: [],
}
