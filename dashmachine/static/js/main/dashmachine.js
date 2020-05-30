
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function js_Load() {
    document.body.style.visibility = 'visible';
}


function updateTabIndicator(){
    sleep(250).then(() => {
        $(".tabs").tabs('updateTabIndicator');
    });
}

function init_select(){
    $('select').formSelect({
        dropdownOptions:{
            container: document.body,
            constrainWidth: true,
        }
    });
    $('input').each(function(index, el) {
        if ($(this).attr('data-autocomplete-options')){
            let options_list = $(this).attr('data-autocomplete-options').split(',');
            let options_dict = options_list.map(x => ({'key': x, 'val': null}));
            options_dict = options_dict.reduce(function(map, obj) {
                map[obj.key] = obj.val;
                return map;
            }, {});
            $(this).autocomplete({
                data: options_dict,
                dropdownOptions:{
                    container: document.body,
                }
            });
            if ($(this).attr('data-auto-only') === 'true') {
                $(this).on('blur', function(e) {
                    if (options_list.includes($(this).val()) === false) {
                        $(this).val('');
                    }
                });
            }
        }
    });
}

// function animateCSS(el, animationName, speed, callback) {
//     el.addClass(`animated ${animationName} ${speed}`);
//
//     function handleAnimationEnd() {
//         el.removeClass(`animated ${animationName} ${speed}`);
//         el.off("animationend");
//
//         if (typeof callback === 'function') callback()
//     }
//
//     el.on("animationend", function () {
//         handleAnimationEnd();
//     })
// }

function init_copy_btn(parent_class){
    $(".copy-btn").on('click', function(e) {
        let target_text = $(this).closest(parent_class).find('.copy-target').text();
        let copy_input = $("#copy-input");
        copy_input.val(target_text);
        copy_input.removeClass("hide");
        copy_input.select();
        document.execCommand("copy");
        copy_input.addClass("hide");
        copy_input.val('');
        M.toast({html: "Copied to Clipboard"})
    });
}

function fetch_settings() {
    $.ajax({
        url: $("#settings-data").attr('data-url'),
        type: 'GET',
        success: function(data){
            $("#settings-data-container").empty();
            $("#settings-data-container").append(data);
            apply_settings();
        }
    });
}

function apply_settings(){
    // Get settings data from inputs
    var settings_background = $("#settings-background").val();
    var settings_theme = $("#settings-theme").val();
    var settings_accent = $("#settings-accent").val();

    var user_background = $("#user-background").val();
    var user_theme = $("#user-theme").val();
    var user_accent = $("#user-accent").val();

    // background
    var bg_to_set = ""
    if (user_background != "None" && user_background.length > 0){
        bg_to_set = user_background
    } else if (settings_background != "None" && settings_background.length > 0){
        bg_to_set = settings_background
    } else {
        bg_to_set = 'none'
    }
    if (bg_to_set.startsWith('#') || bg_to_set.startsWith('var(') ){
        $('body').css("background-color", bg_to_set);
        $('body').css("background-image", 'unset');
    } else if (bg_to_set.toLowerCase() == 'none') {
        $('body').css("background-color", 'var(--theme-background)');
        $('body').css("background-image", 'unset');
    } else {
        $('body').css("background-color", 'unset');
        $('body').css("background-image", `url("${bg_to_set}")`);
    }

    // theme
    if (user_theme != "None" && user_theme.length > 1) {
        localStorage.setItem('mode', user_theme);
        document.documentElement.setAttribute('data-theme', user_theme);
    } else {
        localStorage.setItem('mode', settings_theme);
        document.documentElement.setAttribute('data-theme', settings_theme);
    }
    // accent
    if (user_accent != "None" && user_accent.length > 1) {
        localStorage.setItem('accent', user_accent);
        document.documentElement.setAttribute('data-accent', user_accent);
    } else {
        localStorage.setItem('accent', settings_accent);
        document.documentElement.setAttribute('data-accent', settings_accent);
    }

}

function set_navbar_toggle_pos(){
    let loc_y = parseInt(localStorage.getItem('sidenav-toggle-loc-y'));
    let avail_height = $(window).height() - 146;
    if (loc_y != undefined){
        if (loc_y > avail_height){
            loc_y = avail_height
        }
        $("#sidenav-toggle-svg-container").css({'top': loc_y});
    } else {
        $("#sidenav-toggle-svg-container").css({'top': avail_height});
    }
    $("#sidenav-toggle-svg-container").removeClass('hide');
}




// MODULE SIDENAVS
function load_card_editor() {
    $("#card-editor-sidenav").sidenav({
        edge: 'left',
        inDuration: 350,
        outDuration: 300,
        preventScrolling: false,
        onOpenStart: function () {
            $("#settings-editor-sidenav").sidenav('close');
            $("#config-editor-sidenav").sidenav('close');
            $("#main-sidenav").sidenav('close');
        }
    });
    $.ajax({
        url: $("#card-editor-container").attr('data-url'),
        type: 'GET',
        success: function(data){
            if (data.data != undefined){
                M.toast({html: data.data.msg, classes: "theme-failure"})
            }
            $("#card-editor-container").empty();
            $("#card-editor-container").append(data);
        }
    });
}

function reset_config_editor(){
    $("#config-card-title").text("Config.ini");
    config_textarea_codemirror.setValue($("#config-editor-config-data").val());
    config_textarea_codemirror.toTextArea();
    init_codemirror('properties');
}
function load_config_editor() {
    $("#config-editor-sidenav").sidenav({
        edge: 'left',
        inDuration: 350,
        outDuration: 300,
        preventScrolling: true,
        draggable: false,
        onOpenStart: function () {
            $("#settings-editor-sidenav").sidenav('close');
            $("#card-editor-sidenav").sidenav('close');
            $("#main-sidenav").sidenav('close');
        },
    });
    $.ajax({
        url: $("#config-editor-container").attr('data-url'),
        type: 'GET',
        success: function(data){
            if (data.data != undefined){
                M.toast({html: data.data.msg, classes: "theme-failure"})
            }
            $("#config-editor-container").empty();
            $("#config-editor-container").append(data);
        }
    });
}
var config_textarea_codemirror = ""
function init_codemirror(mode) {
    config_textarea_codemirror = CodeMirror.fromTextArea(document.getElementById("config-textarea"), {
        lineNumbers: true,
        mode: mode,
        theme: 'dashmachine',
        scrollbarStyle: null,
    });
}

function load_settings_editor() {
    $("#settings-editor-sidenav").sidenav({
        edge: 'left',
        inDuration: 350,
        outDuration: 300,
        preventScrolling: false,
        draggable: true,
        onOpenStart: function () {
            $("#config-editor-sidenav").sidenav('close');
            $("#card-editor-sidenav").sidenav('close');
            $("#main-sidenav").sidenav('close');
        }
    });
    $.ajax({
        url: $("#settings-editor-container").attr('data-url'),
        type: 'GET',
        success: function(data){
            if (data.data != undefined){
                M.toast({html: data.data.msg, classes: "theme-failure"})
            }
            $("#settings-editor-container").empty();
            $("#settings-editor-container").append(data);
        }
    });
}

function load_apps(){
    var home_url = $("#home-cards-container").attr("data-url");
    if (home_url != undefined){
        $.ajax({
            url: home_url,
            type: 'GET',
            success: function(data){
                if (data.data != undefined){
                    M.toast({html: data.data.msg, classes: "theme-failure"})
                }
                var container = $("#home-cards-container")
                container.fadeOut(300);
                container.empty();
                container.append(data);
                init_home_cards();
                container.fadeIn(400);
            }
        });
    }

    $.ajax({
        url: $("#sidenav-cards-container").attr("data-url"),
        type: 'GET',
        success: function(data){
            if (data.data != undefined){
                M.toast({html: data.data.msg, classes: "theme-failure"})
            }
            var container = $("#sidenav-cards-container")
            container.fadeOut(300);
            container.empty();
            container.append(data);
            container.fadeIn(400);
        }
    });

}

function toggle_tag_expand(el) {
    if (el.attr("data-expanded") == "true"){
        el.attr("data-expanded", "false");
        el.text('keyboard_arrow_down');
        var tag_row = el.closest('.tag-group').find('.tag-apps-row')
        tag_row.addClass('hide');
    } else {
        el.attr("data-expanded", "true");
        el.text('keyboard_arrow_up');
        var tag_row = el.closest('.tag-group').find('.tag-apps-row')
        tag_row.removeClass('hide');
    }
    var x = 0
    $(".toggle-tag-expand-btn").each(function(e) {
        if ($(this).attr("data-expanded") == "true") {
            x = x + 1
        }
    });
    if (x > 0) {
        $(".toggle-tag-expand-all-btn").text('unfold_less');
    } else {
        $(".toggle-tag-expand-all-btn").text('unfold_more');
    }
}

function hide_empty_tag_groups() {
    $(".tag-group").each(function(i, e) {
        var x = 0
        $(this).find('.app-card').each(function(i, e) {
            if ($(this).hasClass("hide") === false){
                x = x + 1
            }
        });
        if (x === 0){
            $(this).addClass('hide');
        } else {
            $(this).removeClass('hide');
        }
    });
}


//--------------------------------------------------------------------------------------
// Document ready function
//--------------------------------------------------------------------------------------
$(document).ready(function () {
    // var redirect_url = $(".access-group-redirect-url").val()
    // if (redirect_url != undefined){
    //     $(location).attr("href", redirect_url);
    // }
    // console.log($(".access-group-redirect-url").val())

    set_navbar_toggle_pos();

    "use strict";
    apply_settings();

    //  INITS
    init_select();

    $("#update-message-modal").modal({
        dismissible: false
    });
    if ($("#update-message-content").text().length > 1){
        $("#update-message-modal").modal('open');
    }
    $("#update-message-read-btn").on('click', function(e) {
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            success: function(data){
                $("#update-message-modal").modal('close');
            }
        });
    });

    $(".tabs").tabs();

    // Fab
    $(".fixed-action-btn").floatingActionButton();
    $(".fixed-action-btn.horizontal").floatingActionButton({
        direction: "left"
    });
    $(".fixed-action-btn.click-to-toggle").floatingActionButton({
        hoverEnabled: false
    });
    $(".fixed-action-btn.toolbar").floatingActionButton({
        toolbarEnabled: true
    });
    $('.tap-target').tapTarget();
    $('.tap-target').tapTarget('open');

    // Detect touch screen and enable scrollbar if necessary
    function is_touch_device() {
        try {
            document.createEvent("TouchEvent");
            return true;
        } catch (e) {
            return false;
        }
    }
    if (is_touch_device()) {
        $("#nav-mobile").css({
            overflow: "auto"
        });
    }

    // Init collapsible
    $(".collapsible").collapsible({
        accordion: true,
        onOpenStart: function() {
            // Removed open class first and add open at collapsible active
            $(".collapsible > li.open").removeClass("open");
            setTimeout(function() {
                $("#slide-out > li.active > a")
                    .parent()
                    .addClass("open");
            }, 10);
        }
    });
    // make jquery contains selector case unaware
    jQuery.expr[':'].contains = function(a, i, m) {
        return jQuery(a).text().toUpperCase()
            .indexOf(m[3].toUpperCase()) >= 0;
    };

    // MAIN SIDENAV
    $('#main-sidenav').sidenav({
        edge: 'left',
        draggable: true,
        inDuration: 350,
        outDuration: 300,
        preventScrolling: false,
        onCloseStart: function () {
            $("#sidenav-toggle-btn .toggler").attr("data-open", "false");
            $("#sidenav-toggle-btn .toggler").text('list');
        }
    });

    var cursorInPage = false;
    $(window).on('mouseout', function() {
        cursorInPage = false;
    });
    $(window).on('mouseover', function() {
        cursorInPage = true;
    });

    $('#main-sidenav').on('mouseleave', function(e) {
        sleep(100).then(() => {
            if (cursorInPage == true) {
                $("#main-sidenav").sidenav('close');
            }
        });
    });

    $("#sidenav-expand-area-svg").on('mouseenter', function(e) {
        $("#main-sidenav").sidenav('open');
    });
    //
    $("#sidenav-toggle-svg-container").draggable({
        axis: 'y',
        containment: "window",
        iframeFix: true,
    });
    $("#sidenav-toggle-svg-container").on('dragstop', function(event, ui) {
        localStorage.setItem('sidenav-toggle-loc-y', ui.position.top);
    });
    $(window).on('resize', function(e) {
        set_navbar_toggle_pos();
        $("#card-editor-add-btn").dropdown('recalculateDimensions');
    });

    $("#toggle-user-theme-btn").on('click', function(e) {
        var icon_btn = $(this).find('.icon-btn');
        $.ajax({
            url: $(this).attr('data-url'),
            type: 'GET',
            data: {id: $(this).attr("data-user_id"), current_status: icon_btn.text()},
            success: function(data){
                fetch_settings();
                if (icon_btn.text() == "toggle_on"){
                    icon_btn.text('toggle_off');
                    icon_btn.removeClass('theme-primary-text');
                    icon_btn.addClass('theme-secondary-text');
                } else {
                    icon_btn.text('toggle_on');
                    icon_btn.removeClass('theme-secondary-text');
                    icon_btn.addClass('theme-primary-text');
                }
            }
        });
    });


    // ACTION BARS
    var action_providers = {}
    $(".action-provider-span").each(function(e) {
        action_providers[`!${$(this).attr("data-macro")} - ${$(this).attr("data-name")}`] = null
    });

    $(".filter-tags-dropdown-trigger").dropdown({
        constrainWidth: false,
        alignment: 'right',
        coverTrigger: false,
        closeOnClick: false
    });

    $(".filter-tags-dropdown-a").on('click', function(e) {
        var el = $(this);

        $('.filter-tags-dropdown').find('input').each(function(e) {
            if ($(this).attr("data-name") == el.find('input').attr("data-name")){
                if ($(this).prop('checked') == true){
                    $(this).prop('checked', false);
                } else {
                    $(this).prop('checked', true);
                }
            }
        });
        if (el.hasClass('show-all')){
            $('.filter-tags-dropdown').find('input').each(function(e) {
                $(this).prop('checked', false);
            });
        }
        var selected_tags = [];
        el.closest('.filter-tags-dropdown').find('input').each(function(e) {
            if ($(this).prop('checked') == true){
                selected_tags.push($(this).attr("data-name"));
            }
        });
        $(".tag-group").each(function(i, e) {
            var tag_group = $(this);
            if (selected_tags.length < 1){
                tag_group.removeClass('filtered');
                if (tag_group.find('.toggle-tag-expand-btn').attr("data-expanded") == "false"){
                    toggle_tag_expand(tag_group.find('.toggle-tag-expand-btn'));
                }
            } else {
                tag_group.find('.toggle-tag-expand-btn').each(function(e) {
                    $(this).attr("data-expanded", "false");
                    toggle_tag_expand($(this));
                });
                $.each(selected_tags, function(i, e) {
                    if (tag_group.attr("data-tag").indexOf(e) > -1) {
                        tag_group.removeClass('filtered');
                        return false;
                    } else {
                        tag_group.addClass('filtered');
                    }
                });
            }
        });
    });

    $(".action-bar").each(function(e) {
        var action_bar = $(this);

        action_bar.autocomplete({
            data: action_providers,
            onAutocomplete: function () {
                var cut_val = action_bar.val().slice(0, action_bar.val().indexOf('-'))
                action_bar.val(cut_val)
                action_bar.focus();
            }
        });

        action_bar.on('keyup', function(e) {
            if ($(this).val()[0] != "!"){
                var value = ""
                if ($(this).val().length > 1){
                    value = $(this).val().toLowerCase();
                }

                $(".app-card").each(function(e) {
                    var x = 0
                    $(this).find('.searchable').each(function(e) {
                        if ($(this).text().toLowerCase().indexOf(value) > -1) {
                            x = x + 1
                        }
                    });
                    if (x > 0){
                        $(this).removeClass('hide');
                    } else {
                        $(this).addClass('hide');
                    }
                });

                $(".tag-group").each(function(i, e) {
                    var x = 0
                    $(this).find('.app-card').each(function(i, e) {
                        if ($(this).hasClass("hide") === false){
                            x = x + 1
                        }
                    });
                    if (x === 0){
                        $(this).addClass('hide');
                    } else {
                        $(this).removeClass('hide');
                        $(this).find(".toggle-tag-expand-btn").attr('data-expanded', "false")
                        toggle_tag_expand($(this).find(".toggle-tag-expand-btn"));
                    }
                });
            }
        });

        action_bar.on('keydown', function(i, e) {
            if ($(this).val()[0] == "!" && i.which === 13){
                var v = $(this).val();
                var macro = v.slice(0, v.indexOf(' '));
                v = v.replace(`${macro} `, '')
                if (v.length > 0){
                    macro = macro.replace('!', "")
                    var action = ""
                    $(".action-provider-span").each(function(e) {
                        if ($(this).attr("data-macro") == macro){
                            action = $(this).attr("data-action")
                        }
                    });
                    $.ajax({
                        url: $(this).attr('data-search-providers-url'),
                        type: 'GET',
                        data: {action: action, value: v},
                        success: function(data){
                            $(location).attr("href", data);
                        }
                    });
                }
            }
        });

    });

    // TAG EXPAND/COLLAPSE

    if ($("#settings-tags_expanded").val() == "False" || $("#user-tags_expanded").val() == "False"){
        $(".toggle-tag-expand-btn").each(function(e) {
            toggle_tag_expand($(this), false);
        });
        if ($("#user-tags_expanded").val() == "True"){
            $(".toggle-tag-expand-btn").each(function(e) {
                toggle_tag_expand($(this));
            });
        }
    }

    $(".toggle-tag-expand-all-btn").on('click', function(e) {
        if ($(this).text() == "unfold_more") {
            $(".toggle-tag-expand-btn").each(function(e) {
                toggle_tag_expand($(this));
            });
        } else {
            $(".toggle-tag-expand-btn").each(function(e) {
                if ($(this).attr("data-expanded") == "true"){
                    toggle_tag_expand($(this));
                }
            });
        }
    });
});



