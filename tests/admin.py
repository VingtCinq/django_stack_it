from django.contrib import admin
from stack_it.models import Page
from stack_it.admin import PageAdmin as BasePageAdmin

class PageAdmin(BasePageAdmin):
    """
      Admin View for Page
  """

    base_model = Page
    child_models = [Page]
admin.site.register(Page, PageAdmin)
