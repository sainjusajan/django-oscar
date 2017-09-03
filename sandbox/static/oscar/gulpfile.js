
var gulp = require('gulp');
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var csso = require('gulp-csso');
var cleanCSS = require('gulp-clean-css');

gulp.task('scripts', function() {
    return gulp.src([

            
            './js/vendor/jquery-1.12.0.min.js',
            './js/bootstrap.min.js',
            './js/owl.carousel.min.js',
            './js/jquery.meanmenu.js',
            './js/jquery-ui.min.js',
            './js/wow.min.js',
            './js/jquery.mixitup.min.js',
            './js/jquery.magnific-popup.min.js',
            './js/jquery.nivo.slider.js',
            './js/chosen.jquery.min.js',
            './js/jquery.elevateZoom-3.0.8.min.js',
            './js/jquery.countdown.min.js',
            './js/plugins.js'

        ])
        .pipe(concat('saree.js'))
        .pipe(gulp.dest('./js/'));
});

gulp.task('styles', function() {
    return gulp.src([
        './css/bootstrap.min.css',
        './css/animate.css',
        './css/jquery-ui.min.css',
        './css/meanmenu.min.css',
        './css/nivo-slider.css',
        './css/owl.carousel.css',
        './css/font-awesome.min.css',
        './css/pe-icon-7-stroke.css',
        './css/magnific-popup.css',
        './css/chosen.min.css',
        ])
        .pipe(concat('saree.css'))
        .pipe(gulp.dest('./css/'));
});



//pipelining and combination of multiple functions in gulp default
gulp.task('allsass', function(){
    return gulp.src('./scss/scss_styles.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./css/'));
});
gulp.task('alltask', function() {
    return gulp.src([
            './app/assets/frontend/css/raw/plugins.css',
            './app/assets/frontend/css/raw/theme.css',
            './app/assets/frontend/css/raw/icon-fonts.css',
            './app/assets/frontend/css/raw/custom.css',
            './app/assets/frontend/css/raw/slick.css',
            './app/assets/frontend/css/raw/slick-theme.css',
            './app/assets/frontend/css/raw/mixin.css',
            './app/assets/frontend/css/styles.css'
        ])
        // .pipe(watch('./app/assets/frontend/css/*.css'))
        .pipe(concat('jawas1.css'))
        .pipe(csso())
        .pipe(cleanCSS({
            compatibility: 'ie8'
        }))
        .pipe(gulp.dest('./app/assets/frontend/css/'));
});

gulp.task('watch', function() {
    // gulp.watch(['./app/assets/frontend/css/raw/*.*', './app/assets/frontend/css/styles.css'], ['alltask']);
    gulp.watch('./scss/scss_styles.scss', ['allsass']);
});

gulp.task('default', ['allsass', 'alltask', 'watch']);