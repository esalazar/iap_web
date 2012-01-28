$(document).ready(function() {
    $(".login_area").hide();
    $(".show_login").show();

    $(".show_login").click(function() {
       $(".login_area").animate({width: 'toggle'});
       $(".show_login").hide();
    });

    $(".show_related_videos").click(function() {
       $(".related_videos_table").slideToggle();
    });
});
