module.exports = {
  content: [],
  theme: {
    colors: {
        'green': 008000
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
    },
  },
  variants: {
    display: ["responsive", "focus", "dropdown"]
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('tailwindcss-dropdown'),
  ],
}
