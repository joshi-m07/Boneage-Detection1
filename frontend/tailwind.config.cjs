/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx,js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"DM Sans"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace']
      },
      colors: {
        primary: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#b9daf8',
          300: '#85b8ef',
          400: '#4e90e2',
          500: '#2a6fc7',
          600: '#1e5aa8',
          700: '#1a4a8a',
          800: '#1c3f71',
          900: '#1c365e'
        }
      }
    }
  },
  plugins: []
};
