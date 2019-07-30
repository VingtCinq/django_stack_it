from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from stack_it.models import Page
from django.views import View
from django.contrib.sites.shortcuts import get_current_site


class StackItView(View):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request, **kwargs)
        return render(request, self.object.template_path, self.get_context_data())

    def get_object(self, request, *args, **kwargs):
        path = request.path
        if len(path) > 0 and path[-1] != "/":
            path += "/"
        try:
            page = Page.published.get(
                ref_full_path=path, sites=get_current_site(request)
            )
        except Page.DoesNotExist:
            raise Http404()
        return page

    def get_context_data(self, **kwargs):
        ctx = self.object.get_context_data(**kwargs)

        ctx.update({"page": self.object})
        return ctx
