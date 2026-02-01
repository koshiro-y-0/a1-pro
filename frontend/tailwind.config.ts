import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // A1-PRO Color Palette
        primary: {
          DEFAULT: "#3B82F6", // Blue
          dark: "#1E40AF",
        },
        success: "#10B981", // Green
        warning: "#F59E0B", // Orange/Yellow
        danger: "#EF4444",  // Red
        accent: "#8B5CF6",  // Purple
        // Chart colors
        chart: {
          revenue: "#3B82F6",      // Blue
          operating: "#10B981",    // Green
          net: "#F59E0B",          // Orange
          ordinary: "#8B5CF6",     // Purple
          stock: "#1E40AF",        // Dark Blue
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["Roboto Mono", "monospace"],
      },
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [],
} satisfies Config;
