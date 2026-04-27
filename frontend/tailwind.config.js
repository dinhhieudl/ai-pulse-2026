/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        surface: {
          0: "#09090b",
          1: "#111113",
          2: "#18181b",
          3: "#222225",
          4: "#2e2e32",
        },
        accent: {
          DEFAULT: "#818cf8",
          hover: "#a5b4fc",
          muted: "rgba(129,140,248,0.15)",
        },
        success: "#34d399",
        warning: "#fbbf24",
        danger: "#f87171",
        muted: "#71717a",
      },
      fontFamily: {
        sans: [
          "Inter",
          "SF Pro Display",
          "-apple-system",
          "BlinkMacSystemFont",
          "sans-serif",
        ],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      boxShadow: {
        glow: "0 0 20px rgba(129,140,248,0.15)",
        card: "0 1px 3px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05)",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-slow": "pulse 3s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
