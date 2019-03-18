import copy
from django.contrib import admin
from stack_it.models import Page
from stack_it.admin import PageAdmin
from tests_utils.admin import AdminGenericFunctionalTestSet, AdminFunctionalTestSet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

# class PageAdminTest(AdminGenericFunctionalTestSet, AdminFunctionalTestSet):
#     app_label = 'stack_it'
#     model_lower = 'page'
#     model = Page
#     admin = PageAdmin

#     @classmethod
#     def setUpTestData(cls):
#         admin.register(Page, PageAdmin)
#         super(PageAdminTest, cls).setUpTestData()
#         cls.obj =  Page.objects.create(title="Hello", template_path="base.html")

        
