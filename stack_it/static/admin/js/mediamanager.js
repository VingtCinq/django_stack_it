(function($) {
    Dropzone.autoDiscover = false;
    $(function() {
        var mmDropzone = new Dropzone("div#mm-zone", { 
            url: "js/upload",
            paramName: "file"
        });
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        var folder = $('#mm-folder').val();
        $('#mm-folder').change(function() {
            folder = $(this).val();
        })

        mmDropzone.on("sending", function(file, xhr, formData) {
            // Will send the filesize along with the file as POST data.
            formData.append("csrfmiddlewaretoken", csrfToken);
            formData.append('folder', folder);
        });

        $('.js-see').click(function() {
            var url = $(this).data('url');
            window.open(url, '_blank');
        })

        $('.js-edit').click(function() {
            var url = $(this).data('url');
            window.location.href = url;
        })

        $('.js-delete').click(function(evt) {
            evt.preventDefault();
            var $card = $(this).parents().eq(2);
            var pk = $card.data('item');
            $.post( pk + "/js/delete", { 
                csrfmiddlewaretoken: csrfToken
            }, function() {
                $card.remove();
            } );
        })

    })
})(django.jQuery);
