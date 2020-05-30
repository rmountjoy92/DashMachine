sleep(500).then(() => {
    init_codemirror('properties');

    $("#save-config-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            data: {config: config_textarea_codemirror.getValue()},
            success: function(data){
                if (data.data.msg === "success"){
                    M.toast({html: 'Config applied successfully'});
                    $("#config-editor-error-div").closest('.col').addClass('hide');
                    fetch_settings();
                    load_apps();
                    load_card_editor();
                    load_settings_editor();
                } else {
                    $("#config-editor-error-div").empty();
                    $("#config-editor-error-div").closest('.col').removeClass('hide');
                    $("#config-editor-error-div").append(data.data.msg);
                }
            }
        });
    });

    var ctrlDown = false;
    var saved = false;
    $( document ).keydown(function( e ) {
        if (e.key === 'Control') {
            ctrlDown = true;
        }
        if (e.key === 's' && ctrlDown && !saved) {
            e.preventDefault(); // prevent save-as-webpage popup
            saved = true;
            $("#save-config-btn").trigger("click")
        }
    });
    $( document ).keyup(function( e ) {
        if (e.key === 'Control') {
            ctrlDown = false;
        }
        if (e.key === 's' && saved) {
            saved = false;
        }
    });
});