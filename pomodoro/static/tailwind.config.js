/** @type {import('tailwindcss').Config} */
module.exports = {
  content : ['../templates/pomodoro/*.html', './static/**/*.css', './static/**/*.js'],
  theme : {
    extend : {},
  },
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
  plugins : [ require("daisyui") ],
}
