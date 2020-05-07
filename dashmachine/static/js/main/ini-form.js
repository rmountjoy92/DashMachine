// INI FORM
function init_ini_form(container){
    container.find(".ini-form-info-dropdown-trigger").each(function(e) {
        var ini_dropdown_content_id = $(this).closest('.ini-form-info-dropdown-dropdown-container').find('ul').attr('id');
        $(this).dropdown({
            constrainWidth: false,
            closeOnClick: false,
            container: container
        });
        $(this).attr("data-content-id", ini_dropdown_content_id);
    });

    container.find(".ini-form").find('input:not(".hide")').each(function(e) {
        if ($(this).val() == "None"){
            $(this).val("");
        }
        if ($(this).hasClass('ini-form-subvariable-input')){

        } else {
            var id_str = $(this).attr("id").replace("ini-form-", "");
            if ($("#variable-dict-" + id_str).attr("data-variable") == undefined){
                // console.log(id_str + " was hidden")
                $(this).closest('.row').next().remove();
                $(this).closest('.row').remove();
            }
            if ($("#variable-dict-" + id_str).attr("data-disabled") == "True"){
                $(this).prop('disabled', true);
            }
        }
    });
    M.updateTextFields();
    container.find(".ini-form-info-dropdown-trigger").each(function(e) {
        var ini_dropdown_content = $("#" + $(this).attr('data-content-id'));
        var dict_name = $(this).closest('.ini-form-container').attr("data-name");
        var variable_name = $(this).attr("data-name");
        var variable_dict_div = $("#variable-dict-" + dict_name + "-" + variable_name)
        ini_dropdown_content.find('.ini-form-info-variable').text(variable_dict_div.attr("data-variable"));
        ini_dropdown_content.find('.ini-form-info-description').text(variable_dict_div.attr("data-description"));
        ini_dropdown_content.find('.ini-form-info-default').text(variable_dict_div.attr("data-default"));
        ini_dropdown_content.find('.ini-form-info-options').text(variable_dict_div.attr("data-options"));
    });
    container.find(".ini-form-save-btn").on('click', function(e) {
        var form = container.find('.ini-form')
        form.find('input').each(function(e) {
            $(this).prop('disabled', null);
        });
        var unchecked = form.find(':checkbox:not(:checked)');
        unchecked.each(function() {$(this).val('off').prop('checked', true)});
        var formValues = form.serializeArray();
        unchecked.each(function() {$(this).prop('checked', false)});

        var location = $(this).attr('data-location');

        var err_col = form.closest('.ini-form-container').find('.ini-form-error-col');
        var err_div = err_col.find('.ini-form-error-div');

        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            data: formValues,
            success: function(data){
                if (data.data.msg === "success"){
                    err_col.addClass('hide');
                    fetch_settings();
                    load_apps();
                    load_config_editor();
                    load_card_editor();
                    if (location != "settings-editor"){
                        load_settings_editor();
                    }
                    M.toast({html: 'Configuration applied'});
                } else {
                    err_div.empty();
                    err_col.removeClass('hide');
                    err_div.append(data.data.msg);
                }

            }
        });
    });
    // SUBVARIABLES
    $(".ini-form-subvariable-input-add-btn").off('click');
    $(".ini-form-subvariable-input-add-btn").on('click', function(e) {
        var row = $(this).closest('.ini-form-subvariable-set-row');
        var card = row.find('.ini-form-subvariable-set-card').first();
        card.clone().appendTo(row);

        var new_id = Math.floor(Math.random() * 99999) + 10000
        card.find('input').each(function(e) {
            $(this).val('');
            var sliced = $(this).attr('id').slice(0, -5);
            $(this).closest('.input-field').find('label').attr('for', sliced + new_id)
            $(this).attr('id', sliced + new_id);
            $(this).attr('name', sliced + new_id);
            M.updateTextFields();
        });
        init_ini_form(container);
    });
    $(".ini-form-subvariable-delete-btn").off('click');
    $(".ini-form-subvariable-delete-btn").on('click', function(e) {
        var row = $(this).closest('.ini-form-subvariable-set-row');
        var x = 0
        row.find('.ini-form-subvariable-set-card').each(function(e) {
            x = x + 1
        });
        if (x > 1){
            $(this).closest('.ini-form-subvariable-set-card').remove();
            init_ini_form(container);
        }
    });

    // TEMPLATE APPS
    var template_autocomplete_options = {};
    container.find('.card-editor-app-template-options').find('div').each(function(e) {
        template_autocomplete_options[$(this).attr("data-name")] = $(this).attr("data-icon")
    });
    var template_searchbar = container.find('.card-editor-app-template-search')
    template_searchbar.autocomplete({
        data:  template_autocomplete_options,
        minLength: 0,
        onAutocomplete: function () {
            var template_info = $("#app-template-info-" + template_searchbar.val().replace(/ /g, "-"));
            $("#ini-form-App-name").val(template_info.attr("data-name"));
            $("#ini-form-App-prefix").val(template_info.attr("data-prefix"));
            $("#ini-form-App-url").val(template_info.attr("data-url"));
            $("#ini-form-App-sidebar_icon").val(template_info.attr("data-sidebar_icon"));
            $("#ini-form-App-description").val(template_info.attr("data-description"));
            $("#ini-form-App-open_in").val(template_info.attr("data-open_in"));
            $("#ini-form-App-icon").val(template_info.attr("data-icon"));
            template_searchbar.val('');
            M.updateTextFields();
        }
    });
    // DATA SOURCE SELECT
    $("#ini-form-new-ds-selector").on('change', function(e) {
        var form = $("#card-editor-data-sources-form-container")
        var table = $("#card-editor-data-sources-table")
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {platform: $(this).val()},
            success: function(data){
                after_ini_form_ajax_load(form, table, data);
            }
        });
    });

    init_select();

}

function after_ini_form_ajax_load(form, table, data) {
    form.removeClass('hide');
    table.addClass('hide');
    form.empty();
    form.append(data);
    init_ini_form(form);
    form.find(".ini-form-cancel-btn").on('click', function(e) {
        table.removeClass('hide');
        form.addClass('hide');
    });
    form.find('.ini-form-cancel-btn').removeClass('hide');
}