$(document).ready(function() {
    $(".login_area").hide();
    $(".show_login").show();

    $(".show_login").click(function() {
       $(".login_area").animate({width: 'toggle'});
       $(".show_login").hide();
    });

    $(".related_videos").hover(
        function() {
            $(".related_videos_table").show("slide", {direction: "up"});
        },
        function() {
            $(".related_videos_table").hide("slide", {direction: "up"});
        }
    );
});
