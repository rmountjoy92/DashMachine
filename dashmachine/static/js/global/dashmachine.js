
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

function hide_sidenav() {
    $("#main-sidenav").addClass('hide');
    $("#main.main-full").css('padding-left', 0);
    $("#show-sidenav").removeClass('hide');
    localStorage.setItem('sidenav_hidden', 'true');
}

function no_sidebar() {
    $("#main-sidenav").remove();
    $("#main.main-full").css('padding-left', 0);
    $("#no-sidenav").removeClass('hide');
    localStorage.setItem('sidenav_hidden', 'no_sidebar');
}

function show_sidenav(){
    $("#main-sidenav").removeClass('hide');
    $("#main.main-full").css('padding-left', 64);
    $("#show-sidenav").addClass('hide');
    localStorage.setItem('sidenav_hidden', null);
}

function apply_settings(settings){
    // theme
    if (settings['user_theme'] != "None" && settings['user_theme'].length > 1) {
        console.log(settings['user_theme'].length)
        localStorage.setItem('mode', settings['user_theme']);
        document.documentElement.setAttribute('data-theme', settings['user_theme']);
    } else {
        localStorage.setItem('mode', settings['settings_theme']);
        document.documentElement.setAttribute('data-theme', settings['settings_theme']);
    }
    // accent
    if (settings['user_accent'] != "None" && settings['user_accent'].length > 1) {
        localStorage.setItem('accent', settings['user_accent']);
        document.documentElement.setAttribute('data-accent', settings['user_accent']);
    } else {
        localStorage.setItem('accent', settings['settings_accent']);
        document.documentElement.setAttribute('data-accent', settings['settings_accent']);
    }
    if (settings['settings_sidebar_default'] == "closed"){
        localStorage.setItem('sidenav_hidden', 'true');
    } else if (settings['settings_sidebar_default'] == "open"){
        localStorage.setItem('sidenav_hidden', 'false');
    } else if (settings['settings_sidebar_default'] == "no_sidebar"){
        localStorage.setItem('sidenav_hidden', 'no_sidebar');
    }
    if (settings['user_sidebar_default'] == "closed"){
        localStorage.setItem('sidenav_hidden', 'true');
    } else if (settings['user_sidebar_default'] == "open"){
        localStorage.setItem('sidenav_hidden', 'false');
    } else if (settings['user_sidebar_default'] == "no_sidebar"){
        localStorage.setItem('sidenav_hidden', 'no_sidebar');
    }
    if (localStorage.getItem('sidenav_hidden') === 'true'){
        hide_sidenav();
    } else if (localStorage.getItem('sidenav_hidden') === 'no_sidebar'){
        no_sidebar();
    } else if (settings['user_name'].length < 1) {
        no_sidebar();
    }
    // fontawesome
    if (settings['font_awesome'] == "None" || settings['font_awesome'] == "svg" || settings['font_awesome'] == "css") {
        localStorage.setItem('font_awesome', settings['font_awesome']);
    } else {
        localStorage.setItem('font_awesome', 'None');
    }

}

//--------------------------------------------------------------------------------------
// Document ready function
//--------------------------------------------------------------------------------------
$(document).ready(function () {
    "use strict";
    apply_settings({
        settings_theme: $("#settings-theme").val(),
        settings_accent: $("#settings-accent").val(),
        settings_sidebar_default: $("#settings-sidebar_default").val(),
        user_name: $("#user-name").val(),
        user_theme: $("#user-theme").val(),
        user_accent: $("#user-accent").val(),
        user_sidebar_default: $("#user-sidebar_default").val(),
        font_awesome: $("#font-awesome").val(),
    });

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

    $("#hide-sidenav").on('click', function(e) {
        hide_sidenav();
    });

    $("#show-sidenav .material-icons-outlined").on('click', function(e) {
        show_sidenav();
    });

    $( "#show-sidenav" ).draggable({ axis: "y" });

    $(".dropdown-trigger").dropdown({
        coverTrigger: false,
        constrainWidth: false
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

    // mobile sidenav for top-nav layout
    $('.top-nav-mobile-sidenav').sidenav({
        edge: 'right'
    });

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

    // Add open class on init
    $("#slide-out > li.active > a")
        .parent()
        .addClass("open");

    // Open active menu for multi level
    if ($("li.active .collapsible-sub .collapsible").find("a.active").length > 0) {
        $("li.active .collapsible-sub .collapsible")
            .find("a.active")
            .closest("div.collapsible-body")
            .show();
        $("li.active .collapsible-sub .collapsible")
            .find("a.active")
            .closest("div.collapsible-body")
            .closest("li")
            .addClass("active");
    }

    // Auto Scroll menu to the active item
    var position;
    if (
        $(".sidenav-main li a.active")
            .parent("li.active")
            .parent("ul.collapsible-sub").length > 0
    ) {
        position = $(".sidenav-main li a.active")
            .parent("li.active")
            .parent("ul.collapsible-sub")
            .position();
    } else {
        position = $(".sidenav-main li a.active")
            .parent("li.active")
            .position();
    }
    setTimeout(function() {
        if (position !== undefined) {
            $(".sidenav-main ul")
                .stop()
                .animate({ scrollTop: position.top - 300 }, 300);
        }
    }, 300);

    $("#slide-out").sidenav();

    // Collapsible navigation menu
    $(".nav-collapsible .navbar-toggler").click(function() {
        // Toggle navigation expan and collapse on radio click
        if ($(".sidenav-main").hasClass("nav-expanded") && !$(".sidenav-main").hasClass("nav-lock")) {
            $(".sidenav-main").toggleClass("nav-expanded");
            $("#main").toggleClass("main-full");
        } else {
            $("#main").toggleClass("main-full");
        }
        // Set navigation lock / unlock with radio icon
        if (
            $(this)
                .children()
                .text() == "radio_button_unchecked"
        ) {
            $(this)
                .children()
                .text("radio_button_checked");
            $(".sidenav-main").addClass("nav-lock");
            $(".navbar .nav-collapsible").addClass("sideNav-lock");
        } else {
            $(this)
                .children()
                .text("radio_button_unchecked");
            $(".sidenav-main").removeClass("nav-lock");
            $(".navbar .nav-collapsible").removeClass("sideNav-lock");
        }
    });

    // Expand navigation on mouseenter event
    $(".sidenav-main.nav-collapsible, .navbar .brand-sidebar").mouseenter(function() {
        if (!$(".sidenav-main.nav-collapsible").hasClass("nav-lock")) {
            $(".sidenav-main.nav-collapsible, .navbar .nav-collapsible")
                .addClass("nav-expanded")
                .removeClass("nav-collapsed");
            $("#slide-out > li.close > a")
                .parent()
                .addClass("open")
                .removeClass("close");

            setTimeout(function() {
                // Open only if collapsible have the children
                if ($(".collapsible .open").children().length > 1) {
                    $(".collapsible").collapsible("open", $(".collapsible .open").index());
                }
            }, 100);
        }
    });

    // Collapse navigation on mouseleave event
    $(".sidenav-main.nav-collapsible, .navbar .brand-sidebar").mouseleave(function() {
        if (!$(".sidenav-main.nav-collapsible").hasClass("nav-lock")) {
            var openLength = $(".collapsible .open").children().length;
            $(".sidenav-main.nav-collapsible, .navbar .nav-collapsible")
                .addClass("nav-collapsed")
                .removeClass("nav-expanded");
            $("#slide-out > li.open > a")
                .parent()
                .addClass("close")
                .removeClass("open");
            setTimeout(function() {
                // Open only if collapsible have the children
                if (openLength > 1) {
                    $(".collapsible").collapsible("close", $(".collapsible .close").index());
                }
            }, 100);
        }
    });

    // make jquery contains selector case unaware
    jQuery.expr[':'].contains = function(a, i, m) {
        return jQuery(a).text().toUpperCase()
            .indexOf(m[3].toUpperCase()) >= 0;
    };

});



