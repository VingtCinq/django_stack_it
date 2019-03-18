from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.conf.urls import url
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseNotFound
from django.contrib.admin.utils import unquote
from django.utils.safestring import mark_safe

from stack_it.images.forms import ImageForm
from stack_it.images.autocomplete import AutocompleteJsonView


def build_image_thumb(field_name):
    """
    Allow you build image display in admin.

    Args:
        field_name (str): Admin's object field name
    """

    def thumb(self, obj):
        image = getattr(obj, field_name)
        if image:
            return mark_safe(f'<img id="{field_name}_display" src="{image.admin_thumbnail.url}" >')
        return mark_safe(f'<img id="{field_name}_display" src="" alt="No image select">')
    thumb.__name__ = f'{field_name}_display'
    return thumb


class ImageAdmin(admin.ModelAdmin):
    '''Admin View for Image'''

    list_display = ('image', 'created',)
    list_filter = ('folder',)
    form = ImageForm
    # inlines = (
    #     Inline,
    # ]
    # raw_id_fields = ('')
    # readonly_fields = ('')
    actions = None
    search_fields = ('alt', 'image')
    # date_hierarchy = ''
    # ordering = ('')

    def get_urls(self):
        return [
            url(
                r'^js/upload$',
                self.admin_site.admin_view(self.image_upload),
                name='stack_it_image_image_upload',
            ),
            url(
                r'^(.+)/js/delete$',
                self.admin_site.admin_view(self.image_delete),
                name='stack_it_image_image_delete',
            ),
        ] + super(ImageAdmin, self).get_urls()

    def image_upload(self, request, form_url=''):
        if request.method != 'POST':
            return HttpResponseNotFound()
        if not (request.user.is_staff and request.user.has_perm('stack_it.add_image')):
            raise PermissionDenied
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        else:
            return HttpResponseBadRequest(form.errors.as_json())

    def image_delete(self, request, id, form_url=''):
        if request.method != 'POST':
            return HttpResponseNotFound()
        if not (request.user.is_staff and request.user.has_perm('stack_it.delete_image')):
            raise PermissionDenied
        image = self.get_object(request, unquote(id))
        if image is None:
            return HttpResponseNotFound()
        else:
            image.delete()
            return HttpResponse(status=201)

    def autocomplete_view(self, request):
        return AutocompleteJsonView.as_view(model_admin=self)(request)
