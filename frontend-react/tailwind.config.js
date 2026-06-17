/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#071333",
        muted: "#66708d",
        line: "#dbe5f4",
        panel: "#ffffff",
        soft: "#f7faff",
        brand: "#2f6df6",
        brandDark: "#174ecf",
        danger: "#ef3d4c",
        warning: "#f59e1b",
        success: "#34a853"
      },
      boxShadow: {
        card: "0 14px 45px rgba(32, 59, 112, 0.07)"
      },
      fontFamily: {
        sans: ["Inter", "Segoe UI", "Arial", "sans-serif"]
      }
    }
  },
  plugins: []
};
