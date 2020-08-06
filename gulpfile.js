let gulp = require('gulp')
let sass = require('gulp-sass')

function processSass() {
    return gulp
        .src('clubmatcher/static/styles/scss/main.scss')
        .pipe(sass())
        .pipe(gulp.dest('clubmatcher/static/styles/css'))
}

function watch() {
    gulp.watch('clubmatcher/static/styles/scss/**/*.scss', gulp.series(processSass))
}

gulp.task('sass', processSass)
gulp.task('watch', watch)
gulp.task('default', gulp.series(processSass, watch))
