const { series, parallel, src, dest, watch } = require('gulp');
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
const rename = require('gulp-rename')
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer')
const cssnano = require('cssnano');
const tailwind = require('tailwindcss');
const purgeCSS = require('@fullhuman/postcss-purgecss')

function processCustomCss() {
    return src("../dev/css/**/*.css")
        .pipe(postcss([
            autoprefixer(),
            cssnano({
                preset: ['default', {
                    discardComments: {
                        removeAll: true,
                    }
                }]
            })
        ]))
        .pipe(rename({ extname: '.min.css' }))
        .pipe(dest('../prod/css/'))
}

function processCustomJs() {
    return src("../dev/js/**/*.js")
        .pipe(babel())
        .pipe(uglify())
        .pipe(rename({ extname: '.min.js' }))
        .pipe(dest('../prod/js/'))
}

function buildTailwind() {
    return src('./css/tailwind.css')
        .pipe(postcss([
            tailwind(),
            autoprefixer(),
            cssnano({
                preset: ['default', {
                    discardComments: {
                        removeAll: true,
                    }
                }]
            })
        ]))
        .pipe(rename({ extname: '.min.css' }))
        .pipe(dest("./compiled/"))
}


function purgeTailwind() {
    return src('./compiled/tailwind.min.css')
        .pipe(postcss([
            purgeCSS({
                content: [
                    "../../../templates/**/*.html",
                    "../../../templates/store/*.html",
                ],
                defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
            })
        ]))
        .pipe(dest("./compiled/"))
}

function buildMDB() {
    return src('./css/mdb.lite.min.css')
        .pipe(postcss([
            purgeCSS({
                content: [
                    "../../../templates/**/*.html",
                    "../../../templates/store/*.html",
                ],
                defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
            }),
            cssnano({
                preset: ['default', {
                    discardComments: {
                        removeAll: true,
                    }
                }]
            })
        ]))
        .pipe(dest("./compiled/"))
}
function buildBootstrap() {
    return src('./css/bootstrap.min.css')
        .pipe(postcss([
            purgeCSS({
                content: [
                    "../../../templates/**/*.html",
                    "../../../templates/store/*.html",
                ],
                defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
            }),
            cssnano({
                preset: ['default', {
                    discardComments: {
                        removeAll: true,
                    }
                }]
            })
        ]))
        .pipe(dest("./compiled/"))
}

exports.default = parallel(processCustomCss, processCustomJs)
exports.buildGlobalCSS = parallel(buildTailwind, buildMDB, buildBootstrap)
exports.purgeTailwind = purgeTailwind
exports.buildMDB = buildMDB
exports.buildBootstrap = buildBootstrap
