var d = document.getElementById("dashboard-sidenav");
d.className += " active theme-primary";

function get_data_source(el){
    el.html("");
    el.closest('.col').find('.data-source-loading').removeClass('hide');
    $.ajax({
        async: true,
        url: el.attr('data-url'),
        type: 'GET',
        data: {id: el.attr('data-id')},
        success: function(data){
            el.closest('.col').find('.data-source-loading').addClass('hide');
            el.html(data);
        }
    });
}


$( document ).ready(function() {
    $(".tooltipped").tooltip();
    $("#apps-filter").on('keyup', function(e) {
        $(".toggle-tag-expand-btn").each(function(e) {
            if ($(this).attr("data-expanded") == 'false'){
                $(this)[0].click();
            }
        });
        var value = $(this).val().toLowerCase();

        $(".app-card").each(function(e) {
            var x = 0
            $(this).find('.searchable').each(function(e) {
                if ($(this).text().toLowerCase().indexOf(value) > -1) {
                    x = x + 1
                }
            });
            if (x > 0){
                $(this).removeClass('hide');
            } else {
                $(this).addClass('hide');
            }
        });

        $(".tag-group").each(function(i, e) {
            var x = 0
            $(this).find('.app-card').each(function(i, e) {
                if ($(this).hasClass("hide") === false){
                    x = x + 1
                }
            });
            if (x === 0){
                $(this).addClass('hide');
            } else {
                $(this).removeClass('hide');
            }
        });
    });

    $(".data-source-container").each(function(e) {
        get_data_source($(this));
    });

    $(".refresh-data-source-btn").on('click', function(e) {
        e.preventDefault();
        $(this).closest('.app-card').find(".data-source-container").each(function(e) {
            get_data_source($(this));
        });
    });

    $("#tags-select").on('change', function(e) {
        var value = $(this).val();
        $(".tag-group").each(function(i, e) {
            if ($(this).find('.toggle-tag-expand-btn').attr("data-expanded") == "false"){
                $(this).find('.toggle-tag-expand-btn')[0].click();
            }
            if ($(this).attr("data-tag").indexOf(value) > -1 || value === "All tags") {
                $(this).removeClass('filtered');
            } else {
                $(this).addClass('filtered');
            }
        });
    });

    $(".toggle-tag-expand-btn").on('click', function(e) {
        if ($(this).attr("data-expanded") == "true"){
            $(this).attr("data-expanded", "false");
            $(this).text('keyboard_arrow_down');
            $(this).closest('.tag-group').find('.tag-apps-row').addClass('hide');
        } else {
            $(this).attr("data-expanded", "true");
            $(this).text('keyboard_arrow_up');
            $(this).closest('.tag-group').find('.tag-apps-row').removeClass('hide');
        }
        var x = 0
        $(".toggle-tag-expand-btn").each(function(e) {
            if ($(this).attr("data-expanded") == "true") {
                x = x + 1
            }
        });
        if (x > 0) {
            $("#toggle-tag-expand-all-btn").text('unfold_less');
        } else {
            $("#toggle-tag-expand-all-btn").text('unfold_more');
        }
    });

    $("#toggle-tag-expand-all-btn").on('click', function(e) {
        if ($(this).text() == "unfold_more") {
            $(".toggle-tag-expand-btn").each(function(e) {
                $(this)[0].click();
            });
        } else {
            $(".toggle-tag-expand-btn").each(function(e) {
                if ($(this).attr("data-expanded") == "true"){
                    $(this)[0].click();
                }
            });
        }
    });

    if ($("#settings-tags_expanded").val() == "False" || $("#user-tags_expanded").val() == "False"){
        $(".toggle-tag-expand-btn").each(function(e) {
            $(this)[0].click();
        });
        if ($("#user-tags_expanded").val() == "True"){
            $(".toggle-tag-expand-btn").each(function(e) {
                $(this)[0].click();
            });
        }
    }

});