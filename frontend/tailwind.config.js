// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        purple: {
          600: '#8B5CF6', // 主要品牌色
          700: '#7C3AED', // 深色變體
          200: '#DDD6FE', // 淺色變體
        }
      },
      animation: {
        bounce: 'bounce 1s infinite',
      }
    },
  },
  plugins: [],
}