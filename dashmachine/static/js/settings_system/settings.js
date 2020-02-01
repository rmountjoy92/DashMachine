var d = document.getElementById("settings-sidenav");
d.className += " active theme-primary";

$( document ).ready(function() {
    initTCdrop('#images-tcdrop');
    $("#config-wiki-modal").modal();

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
                    M.toast({html: data.data.msg, classes: "theme-warning"});
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

    $("#update-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            success: function(data){
                M.toast({html: 'DashMachine Updated'});
                $("#update-btn").addClass('hide');
                $("#check-update-btn").removeClass('hide');
            }
        });
    });

    $("#check-update-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            success: function(data){
                if (data === "True"){
                    $("#update-btn").removeClass('hide');
                    $("#check-update-btn").addClass('hide');
                } else {
                    M.toast({html: 'Up to date!'});
                }
            }
        });
    });

    $("#edit-user-btn").on('click', function(e) {
       $.ajax({
           url: $(this).attr('data-url'),
           type: 'POST',
           data: $("#edit-user-form").serialize(),
           success: function(data){
               if (data.data.err !== 'success'){
                   M.toast({html: data.data.err, classes: 'theme-warning'});
               } else {
                   $("#user-form-password").val('');
                   $("#user-form-confirm_password").val('');
                   M.toast({html: 'User updated'});
               }
           }
       });
    });

});