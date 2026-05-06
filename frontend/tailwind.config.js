export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b1020",
        panel: "rgba(15, 23, 42, 0.76)",
        accent: "#14b8a6",
        flame: "#fb7185"
      },
      boxShadow: {
        glow: "0 24px 80px rgba(20, 184, 166, 0.14)"
      }
    }
  },
  plugins: [],
};
