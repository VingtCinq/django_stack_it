from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from stack_it.models import Page
from django.views import View


class StackItView(View):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request, **kwargs)
        return render(request, self.object.template_path, self.get_context_data())

    def get_object(self, request, *args, **kwargs):
        path = request.get_full_path()
        print(path)
        if len(path) > 0 and path[-1] != "/":
            path += "/"
        try:
            page = Page.objects.get(ref_full_path=path)
        except Page.DoesNotExist:
            raise Http404()
        return page

    def get_context_data(self, **kwargs):
        ctx = self.object.get_context_data(**kwargs)
        print(ctx)
        
        ctx.update({"page": self.object})
        return ctx
