
init = function ($) {
    function handleLoginRequired(login_required, field_allowed_groups) {
        if (login_required.is(':checked')) {
            field_allowed_groups.slideDown();
        }
        else {
            field_allowed_groups.slideUp();

        }
    }

    function handlePermissions(login_required) {
        var selected_groups = $('#id_allowed_groups_to'),
            options_selected = selected_groups.find('option').length > 0;
        if (options_selected) {
            login_required.attr("disabled", true);
            login_required.attr("checked", true);
        } else {
            login_required.attr("disabled", false);
        }
    }

    var login_required = $('#id_login_required'),
        field_allowed_groups = $('.field-allowed_groups');

    handleLoginRequired(login_required, field_allowed_groups)

    login_required.click(function () {
        handleLoginRequired(login_required, field_allowed_groups)
    })

    redisplay = SelectBox.redisplay;
    SelectBox.redisplay = function (e) {
        redisplay(e)
        if (e == 'id_allowed_groups_to') {
            handlePermissions(login_required);
        }
    }

}
window.onload = function () {
    init(django.jQuery)
};