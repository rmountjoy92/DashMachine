
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function js_Load() {
    document.body.style.visibility = 'visible';
}

function init_datepicker() {
    $('.datepicker').datepicker({
        container: 'body',
        format: 'mm/dd/yy'
    });
}
function init_timepicker() {
    $('.timepicker').timepicker({
        container: 'body'
    });
}
// toggle/init tooltips
function init_tooltips(){
    let tooltips_enabled = localStorage.getItem('tooltips_enabled');
    if (tooltips_enabled === 'false'){
    } else {
        $('.tooltipped').tooltip();
    }
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

function loadContactForm(){
    let url = $("#load-contact-form-url").attr('data-url');
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data){
            $('body').append(data);
            init_select();
        }
    });
}

function autocomplete_chips_add_function(el_id, el){
    let instance = M.Chips.getInstance(el);
    let val_list = []
    $.each(instance.chipsData, function(index, el) {
        val_list.push(el.tag);
    });
    let hidden_inp = `#${el_id.split('-')[1]}`
    $(hidden_inp).val(val_list.toString());
    // console.log($(hidden_inp).val());
    $(`#${el_id} input`).trigger('focus');
}

function init_autocomplete_chips(){
    $(".chips").each(function(index, el) {
        let el_id = $(this).attr('id');
        let el_this = $(this);
        $(this).chips({
            placeholder: $(this).attr('data-placeholder'),
            secondaryPlaceholder: $(this).attr('data-second-placeholder'),
            limit: $(this).attr('data-limit'),
            autocompleteOptions: {
                data: null,
            },
            onChipAdd: function (){
                autocomplete_chips_add_function(el_id, el);
                $("#deal-form-default-fields").trigger('change');
            },
            onChipDelete: function () {
                autocomplete_chips_add_function(el_id, el);
                $("#deal-form-default-fields").trigger('change');
            },
        });

        let hidden_inp = `#${el_id.split('-')[1]}`
        if ($(hidden_inp).val() !== "None") {
            let instance = M.Chips.getInstance($(this));
            let contacts = $(hidden_inp).val();
            contacts = contacts.split(',');
            $.each(contacts, function(index, el) {
                instance.addChip({
                    tag: el,
                });
            });
        }
        $(`#${el_id} input`).on('keydown', function(e) {
            let instance = M.Chips.getInstance(el_this);
            let keyCode = e.keyCode || e.which;
            if (keyCode == 9) {
                let option = $(el_this).find('.autocomplete-content li').first()
                if (option.length > 0) {
                    instance.autocomplete.selectOption(option);
                    e.preventDefault();
                }
            }
        });

        $(`#${el_id} input`).on('keyup', function(e) {
            let instance = M.Chips.getInstance(el_this);
            let keyCode = e.keyCode || e.which;
            let ign_codes = [40, 38, 37, 39, 16, 9, 20, 17, 18, 32]
            if (ign_codes.includes(keyCode)) {}
            else {
                $.ajax({
                    url: $("#load-autocomplete-contacts-url").attr('data-url'),
                    type: 'GET',
                    data: {
                        contact_group: $(`#${el_id}`).attr('data-contact_group'),
                        inp_val: $(this).val(),
                    },
                    success: function(data){
                        instance.autocomplete.updateData(data);
                        sleep(100).then(() => {
                            instance.autocomplete.open();
                        });
                    }
                });
            }
        });

        $(`#${el_id} input`).on('blur', function() {
            let instance = M.Chips.getInstance(el_this);
            sleep(250).then(() => {
                if (instance.chipsData.length < 1 && $(this).val().length > 0){
                    $(this).val('');
                    M.toast({html: "Press enter to add a contact"})
                }
            });

        });

    });
}

function init_send_doc_email_btns(el) {
    el.on('click', function() {
        let attachment_deal = $("#attachment-deal")
        attachment_deal.val($(this).attr('data-deal_id'));
        attachment_deal.trigger('change');
        sleep(100).then(() => {
            let deal_doc = $("#deal-doc")
            deal_doc.val($(this).attr('data-file'));
            deal_doc.trigger('change');
            tinymce.get("email-panel-content").setContent($(this).attr('data-signature'));
            $("#attachments").removeClass('hide');
            $("#email-panel").removeClass('hide');
            $("#chips-mailto input").trigger('focus');
        });
    });
}

function toggleDarkMode(){
    let mode = localStorage.getItem('mode');
    if (mode === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('mode', null);
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('mode', 'dark');
    }
    // location.reload(true);
}

function toggleTooltips(){
    let tooltips_enabled = localStorage.getItem('tooltips_enabled');
    if (tooltips_enabled === 'false'){
        localStorage.setItem('tooltips_enabled', null);
        $('.tooltipped').tooltip();
    } else {
        localStorage.setItem('tooltips_enabled', 'false');
        try {
            $(".tooltipped").tooltip('destroy');
        } catch (e) {}
    }
}

function init_copy_btn(){
    $(".copy-btn").on('click', function(e) {
        let target_text = $(this).closest('.col').find('.copy-target').text();
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

function isEmail(email) {
    let regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

// Cleave
function initCleave(){
    // prevent database from filling inputs with "None"
    $("input").each(function(e) {
        if($(this).val() === "None"){
            $(this).val('');
        }
    });
    M.updateTextFields();
    document.querySelectorAll('.input-phone').forEach(function (el) {
        new Cleave(el, {
            phone: true,
            phoneRegionCode: 'US',
            delimiter: '-',
        });
    });
    document.querySelectorAll('.money').forEach(function (el) {
        new Cleave(el, {
            numeral: true,
            numeralThousandsGroupStyle: 'thousand',
            prefix: '$',
            noImmediatePrefix: true,
            numeralPositiveOnly: true
        });
    });
    document.querySelectorAll('.days').forEach(function (el) {
        new Cleave(el, {
            blocks: [2],
            numericOnly: true,
        });
    });
    document.querySelectorAll('.datepicker').forEach(function (el) {
        new Cleave(el, {
            date: true,
            delimiter: '/',
            datePattern: ['m', 'd', 'y']
        });
    });
    document.querySelectorAll('.zip_code').forEach(function (el) {
        new Cleave(el, {
            blocks: [5],
            numericOnly: true,
        });
    });
    document.querySelectorAll('.initial').forEach(function (el) {
        new Cleave(el, {
            blocks: [1],
        });
    });
    document.querySelectorAll('.state').forEach(function (el) {
        new Cleave(el, {
            blocks: [2],
            uppercase: true
        });
    });
    document.querySelectorAll('.number').forEach(function (el) {
        new Cleave(el, {
            numeral: true
        });
    });
}

// TinyMCE Editor
function initTinyMCE(el){
    // Check TinyMCE initialized or not
    if(tinyMCE.get(el)){
        // Remove instance by id
        tinymce.remove('#' + el);
    }else{
        let mode = localStorage.getItem('mode');
        let theme = ""
        if (mode === 'dark') {
            theme = "dark"
        } else {
            theme = "light"
        }
        tinymce.init({
            selector: '#' + el,
            height: 200,
            menubar: false,
            removed_menuitems: 'undo, redo, anchor',
            skin: theme,
            statusbar: true,
            branding: false,
            paste_data_images: true,
            force_br_newlines: true,
            force_p_newlines: false,
            forced_root_block: '',
            content_style: "body {margin-top: 15px}",
            visual_table_class: 'no-border',
            mode: "exact",
            plugins: [
                'autolink lists link image charmap print preview anchor textcolor',
                'searchreplace visualblocks code fullscreen',
                'insertdatetime media table paste code help imagetools'
            ],
            toolbar: 'formatselect | bold italic forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent fullscreen code',
            content_css: [
                '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
                '//www.tiny.cloud/css/codepen.min.css'
            ]
        });
    }
}

//--------------------------------------------------------------------------------------
// Document ready function
//--------------------------------------------------------------------------------------
$(document).ready(function () {
    "use strict";

    //  INITS
    init_datepicker();
    init_timepicker();
    initCleave();
    init_tooltips();
    init_copy_btn();
    init_select();
    $(".dropdown-trigger").dropdown({
        coverTrigger: false,
        constrainWidth: false
    });
    $(".tabs").tabs();
    $(".scrollspy").scrollSpy();

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



