$(document).ready(function(){
    $('#mobile-demo').sidenav();
    $("#md-container").find('a').on('click', function(e) {
        sleep(100).then(() => {
            var y = $(window).scrollTop();
            $(window).scrollTop(y-185);
        });
    });
});