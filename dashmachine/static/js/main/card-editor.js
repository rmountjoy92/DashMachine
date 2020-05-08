// CARD EDITOR
$("#card-editor-open-btn").on('click', function(e) {
    $('#main-sidenav').sidenav('close');
});
$(".show-card-editor-data-sources-table").on('click', function(e) {
    $("#card-editor-cards-table").addClass('hide');
    $("#card-editor-data-sources-table").removeClass('hide');
});
$(".show-card-editor-cards-table").on('click', function(e) {
    $("#card-editor-cards-table").removeClass('hide');
    $("#card-editor-data-sources-table").addClass('hide');
});

$("#card-editor-add-btn").dropdown({
    container: '#card-editor-sidenav',
    constrainWidth: false,
    onOpenStart: function () {
        $(".card-editor-add-dropdown-overlay").removeClass('hide');
    },
    onCloseStart: function () {
        $(".card-editor-add-dropdown-overlay").addClass('hide');
    }
});
$("#card-editor-data-source-add-btn").dropdown({
    container: '#card-editor-sidenav',
    constrainWidth: false,
    onOpenStart: function () {
        $(".card-editor-add-dropdown-overlay").removeClass('hide');
    },
    onCloseStart: function () {
        $(".card-editor-add-dropdown-overlay").addClass('hide');
    }
});

$(".card-editor-app-row").on('click', function(e) {
    var form = $("#card-editor-form-container")
    var table = $("#card-editor-cards-table")
    $.ajax({
        url: $(this).attr('data-url'),
        type: 'GET',
        data: {app_id: $(this).attr('data-id')},
        success: function(data){
            after_ini_form_ajax_load(form, table, data);
        }
    });
});
$(".card-editor-data-source-row").on('click', function(e) {
    var form = $("#card-editor-data-sources-form-container")
    var table = $("#card-editor-data-sources-table")
    $.ajax({
        url: $(this).attr('data-url'),
        type: 'GET',
        data: {ds_id: $(this).attr('data-id')},
        success: function(data){
            after_ini_form_ajax_load(form, table, data);
        }
    });
});
$(".card-editor-add-dropdown-a").on('click', function(e) {
    var form = $("#card-editor-form-container")
    var table = $("#card-editor-cards-table")
    $.ajax({
        url: $("#card-editor-add-dropdown").attr('data-url'),
        type: 'GET',
        data: {type: $(this).attr('data-type')},
        success: function(data){
            after_ini_form_ajax_load(form, table, data);
        }
    });
});
$("#card-editor-add-new-ds-btn").on('click', function(e) {
    var form = $("#card-editor-data-sources-form-container")
    var table = $("#card-editor-data-sources-table")
    $.ajax({
        url: $(this).attr('data-url'),
        type: 'GET',
        success: function(data){
            after_ini_form_ajax_load(form, table, data);
        }
    });
});