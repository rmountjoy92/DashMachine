function reset_config_editor(){
    $("#config-card-title").text("Config.ini");
    $("#save-config-btn").removeClass('hide');
    $("#save-editing-wiki-btn").addClass('hide');
    $("#wiki-config-form").addClass('hide');
    config_textarea_codemirror.toTextArea();
    $("#config-textarea").val($("#config-editor-config-data").val());
    init_codemirror('properties');
}

$( document ).ready(function() {
    $("#edit-wiki-btn").on('click', function(e) {
        config_textarea_codemirror.setValue($(this).attr("data-md"));
        config_textarea_codemirror.toTextArea();
        init_codemirror('markdown');
        $("#wiki-config-form-permalink").val($(this).attr('data-permalink'));
        $("#wiki-config-form-permalink-new").val($(this).attr('data-permalink'));
        $("#wiki-config-form-name").val($(this).attr('data-name'));
        $("#wiki-config-form-author").val($(this).attr('data-author'));
        $("#wiki-config-form-description").val($(this).attr('data-description'));
        $("#wiki-config-form-tags").val($(this).attr('data-tags'));
        M.updateTextFields();
        $("#wiki-config-form").removeClass('hide');


        $("#config-editor-sidenav").sidenav('open');
        $("#save-config-btn").addClass('hide');
        $("#save-editing-wiki-btn").removeClass('hide');
        $("#config-card-title").text(`Editing ${$(this).attr("data-name")}`);
        $("#close-config-editor-sidenav").one('click', function (e) {
            reset_config_editor();
        })

        $("#save-editing-wiki-btn").on('click', function(e) {
            M.toast({html: "Reloading.."})
            config_textarea_codemirror.save();
            $.ajax({
                url: $(this).attr('data-url'),
                type: 'POST',
                data: $("#config-form").serialize(),
                success: function(data){
                    location.reload();
                }
            });
        });
    });
});