sleep(500).then(() => {
    var config_textarea_codemirror = CodeMirror.fromTextArea(document.getElementById("config-textarea"), {
        lineNumbers: true,
        mode: 'properties',
        theme: 'dashmachine',
        scrollbarStyle: null,
    });

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
});