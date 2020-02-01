var d = document.getElementById("dashboard-sidenav");
d.className += " active theme-primary";


$( document ).ready(function() {
    $("#apps-filter").on('keyup', function(e) {
        var value = $(this).val().toLowerCase();
        $(".app-a").each(function(i, e) {
            if ($(this).attr("data-name").toLowerCase().indexOf(value) > -1
                || $(this).attr("data-description").toLowerCase().indexOf(value) > -1) {
                $(this).removeClass('hide');
            } else {
                $(this).addClass('hide');
            }
        });
    });

    $(".data-template").each(function(e) {
        var el = $(this);
        $.ajax({
            url: el.attr('data-url'),
            type: 'GET',
            data: {template: el.text()},
            success: function(data){
                el.text(data);
                el.removeClass('hide');
            }
        });
    });
});