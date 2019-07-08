(function ($) {
    "use strict";
    function format(data) {
        if (data.image) {
            return "<img src='" + data.src + "'/>";
        } else {
            return data.text
        }

    }
    var init = function ($element, options, select) {
        var settings = $.extend(options, {
            ajax: {
                data(params) {
                    return {
                        term: params.term,
                        page: params.page
                    };
                }
            },
            templateResult: format,
            escapeMarkup(m) {
                return m;
            },


        });
        $element.select2(settings);
        $element.on("select2:select", select);
    };

    $.fn.djangoAdminSelect2 = function (options) {
        var settings = $.extend({}, options);
        function select(event) {
            var src = event.params.data.src,
                image = event.params.data.image,
                $select = $(event.target)[0],
                $parent = $select.closest("tr.form-row");
            if ($parent) {
                var name = $select.name.split("-")[$select.name.split("-").length - 1];
                var $images = $($parent).find("#" + name + "_display");
            } else {
                var $images = $("#" + $select.name + "_display");
            }

            if (image) {
                $.each($images, function (i, element) {
                    var $element = $(element);
                    $element.attr("src", src);
                })
            };

        };
        $.each(this, function (i, element) {
            var $element = $(element);
            init($element, settings, select);
        });
        return this;
    };

    $(function () {
        // Initialize all autocomplete widgets except the one in the template
        // form used when a new formset is added.
        $(".admin-autocomplete").not("[name*=__prefix__]").djangoAdminSelect2();
    });

    $(document).on("formset:added", (function () {
        return function (event, $newFormset) {
            return $newFormset.find(".admin-autocomplete").djangoAdminSelect2();
        };
    })(this));
}(django.jQuery));
