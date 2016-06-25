var gulp = require('gulp')
var concat = require('gulp-concat')

gulp.task('scripts', function() {
  return gulp.src('./frontend/js/*.js')
    .pipe(concat('hanabira.js'))
    .pipe(gulp.dest('./hanabira/public/js/'))
})
