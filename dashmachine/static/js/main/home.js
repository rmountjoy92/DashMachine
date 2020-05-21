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

    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        $(".expandable-card").addClass('scrollbar');
    } else {
        $(".expandable-card").on('mouseenter', function(e) {
            var tag_row = $(this).closest('.tag-apps-row');
            tag_row.css("min-height", tag_row.height());

            var column = $(this).closest('.col')
            column.css('min-width', column.width());
            column.css('min-height', column.height());

            var width = $(this).width();
            $(this).css("position", "absolute");
            $(this).css("max-height", "unset");
            $(this).css("overflow", "auto");
            $(this).css("height", "auto");
            $(this).css("width", width);
            $(this).css("z-index", 888);
        });
        $(".expandable-card").on('mouseleave', function(e) {
            var tag_row = $(this).closest('.tag-apps-row');
            tag_row.css("min-height", "unset");

            var column = $(this).closest('.col');
            column.css('min-width', "unset");
            column.css('min-height', "unset");

            var width = $(this).width()
            $(this).css("position", "relative");
            $(this).css("max-height", "146px");
            $(this).css("overflow", "hidden");
            $(this).css("height", "146px");
            $(this).css("width", "unset");
            $(this).css("z-index", 1);
        });
    }
}


$( document ).ready(function() {
    $(".tooltipped").tooltip();

    init_home_cards();

    $(".card-editor-add-from-home-btn").on('mouseenter', function(e) {
        $('body')[0].click();
    });

    $(".card-editor-add-from-home-btn").on('click', function(e) {
        $("#card-editor-data-sources-form-container").addClass('hide');
        $("#card-editor-data-sources-table").addClass('hide');
        $("#card-editor-form-container").removeClass('hide');
        $("#card-editor-cards-table").removeClass('hide');

        sleep(250).then(() => {
            $("#card-editor-add-btn").dropdown('open');
        });
    });

    $('#add-new-app-tap-target').tapTarget();
    $('#add-new-app-tap-target').tapTarget('open');

});