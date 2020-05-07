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

function init_home_cards(){
    $(".data-source-container").each(function(e) {
        get_data_source($(this));
    });

    $(".refresh-data-source-btn").on('click', function(e) {
        e.preventDefault();
        $(this).closest('.app-card').find(".data-source-container").each(function(e) {
            get_data_source($(this));
        });
    });

    $(".tag-group-btn").off('click');
    $(".tag-group-btn").on('click', function(e) {
        var tag_name = $(this).closest('.tag-group').attr("data-tag");
        $(".toggle-tag-expand-btn").each(function(e) {
            if ($(this).closest('.tag-group').attr("data-tag") == tag_name){
                toggle_tag_expand($(this));
            }
        });
    });
}


$( document ).ready(function() {
    $(".tooltipped").tooltip();

    init_home_cards();

});