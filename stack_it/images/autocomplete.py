from django.contrib.admin.views.autocomplete import AutocompleteJsonView as BaseAutocompleteJsonView
from django.http import Http404, JsonResponse


class AutocompleteJsonView(BaseAutocompleteJsonView):

    """Overriding AutocompleteJsonView to allow safe snippets

    Attributes:
        object_list (TYPE): Description
        paginator_class (TYPE): Description
        term (TYPE): Description
    """

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """
        if not self.model_admin.get_search_fields(request):
            raise Http404(
                '%s must have search_fields for the autocomplete_view.' %
                type(self.model_admin).__name__
            )
        if not self.has_perm(request):
            return JsonResponse({'error': '403 Forbidden'}, status=403)

        self.term = request.GET.get('term', '')
        self.paginator_class = self.model_admin.paginator
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        autocomplete_image = hasattr(self.model_admin.model, 'autocomplete_image')
        return JsonResponse({
            'results': [
                {'id': str(obj.pk),
                 'image': autocomplete_image,
                 'text': str(obj),
                 'src': obj.autocomplete_image if autocomplete_image else str(obj),
                 }
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })
