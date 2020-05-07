
$( document ).ready(function() {
    $(".tabs").tabs();

    init_ini_form($("#settings-editor-settings-form-container"));

    init_select();

    initTCdrop('#images-tcdrop');

    $(".settings-editor-ag-row").on('click', function(e) {
        var table = $("#settings-editor-ag-table")
        var form = $("#settings-editor-ag-form-container")
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {ag_id: $(this).attr('data-id')},
            success: function(data){
                after_ini_form_ajax_load(form, table, data);
            }
        });
    });

    $(".settings-editor-user-row").on('click', function(e) {
        var table = $("#settings-editor-user-table")
        var form = $("#settings-editor-user-form-container")
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {user_id: $(this).attr('data-id')},
            success: function(data){
                after_ini_form_ajax_load(form, table, data);
            }
        });
    });

    $("#save-images-btn").on('click', function(e) {
        $("#add-images-input").val(tcdrop_files['images-tcdrop'].toString());
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            data: $("#add-images-form").serialize(),
            success: function(data){
                $("#add-images-form").trigger('reset');
                $("#files-div").empty();
                $("#files-div").append(data);
                tcdropResetAll();
            }
        });
    });

    $(".settings-editor-add-ag-btn").on('click', function(e) {
        var table = $("#settings-editor-ag-table")
        var form = $("#settings-editor-ag-form-container")
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {new: "True"},
            success: function(data){
                after_ini_form_ajax_load(form, table, data);
            }
        });
    });

    $(".settings-editor-add-user-btn").on('click', function(e) {
        var table = $("#settings-editor-user-table")
        var form = $("#settings-editor-user-form-container")
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {new: "True"},
            success: function(data){
                after_ini_form_ajax_load(form, table, data);
            }
        });
    });
});