module.exports = {
  plugins: [
    require("tailwindcss"),
    require("autoprefixer"),
    require("@fullhuman/postcss-purgecss")({
      content: [
        "../../../templates/**/*.html",
        "../../../templates/store/*.html",
      ],
      defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
    })
  ]
}

// purgecss --css static/store/Tailwind/tailwind.css --content templates/**/*.html --*/*.html --output static/store/Tailwind/tailwindp.css