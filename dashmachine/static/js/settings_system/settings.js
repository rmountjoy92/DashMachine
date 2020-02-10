var d = document.getElementById("settings-sidenav");
d.className += " active theme-primary";

$( document ).ready(function() {
    $("#config-readme table").addClass('responsive-table');
    initTCdrop('#images-tcdrop');
    $("#user-modal").modal({
        onCloseEnd: function () {
            $("#edit-user-form").trigger('reset');
        }
    });

    $("#save-config-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            data: $("#config-form").serialize(),
            success: function(data){
                if (data.data.msg === "success"){
                    M.toast({html: 'Config applied successfully'});
                    location.reload(true);
                } else {
                    M.toast({html: data.data.msg, classes: "theme-failure"});
                }
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

    var template_apps = $("#templates-filter").attr("data-template_apps").split(',');
    var autocomplete_data = {}
    $.each(template_apps, function(i, e) {
        autocomplete_data[e.split('&&')[0]] = e.split('&&')[1]
    });

    $("#templates-filter").autocomplete({
        limit: 16,
        data: autocomplete_data,
        onAutocomplete: function () {
            $.ajax({
                url: $("#templates-filter").attr('data-url'),
                type: 'GET',
                data: {name: $("#templates-filter").val()},
                success: function(data){
                    $("#template-div").empty();
                    $("#template-div").append(data);
                }
            });
        }
    });

    $("#save-user-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'POST',
            data: $("#edit-user-form").serialize(),
            success: function(data){
                if (data.data.err !== 'success'){
                    M.toast({html: data.data.err, classes: 'theme-failure'});
                } else {
                    $("#users-div").empty();
                    $("#users-div").append(data.data.html);
                    $("#user-modal").modal('close');
                    M.toast({html: 'User saved'});
                }
            }
        });
    });

});