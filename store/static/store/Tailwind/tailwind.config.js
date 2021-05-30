module.exports = {
  purge: [
    "../../../templates/**/*.html",
    "../../../templates/store/**/*.html",
    "../../../../**/*.html"
  ],
  prefix: "tw-",
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      width: {
        "104": "26rem",
        "112": "28rem",
        "120": "30rem"
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@fullhuman/postcss-purgecss")
  ],
}
