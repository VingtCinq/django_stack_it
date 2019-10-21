from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from stack_it.models import Page
from django.views import View
from django.contrib.sites.shortcuts import get_current_site


class StackItView(View):
    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        self.object = self.get_object(request, current_site, **kwargs)
        if (
            hasattr(self.object, "main_site_id")
            and self.object.main_site_id is not None
            and self.object.main_site_id != current_site.id
        ):
            return redirect(self.object.main_site.domain + self.object.ref_full_path)
        return render(request, self.object.template_path, self.get_context_data())

    def get_object(self, request, current_site, *args, **kwargs):
        path = request.path
        if len(path) > 0 and path[-1] != "/":
            path += "/"
        try:
            page = Page.published.get(ref_full_path=path, sites=current_site)
        except Page.DoesNotExist:
            raise Http404()
        return page

    def get_context_data(self, **kwargs):
        ctx = self.object.get_context_data(**kwargs)
        ctx.update({"page": self.object})
        return ctx


def key_redirect(request, key):
    page = Page.objects.get(key=key)
    return redirect(page.ref_full_path, permanent=True)


def sitemap(request):
    current_site = get_current_site(request)
    pages = Page.published.filter(sites=current_site)
    return render(
        request,
        "stack_it/sitemap.html",
        {"current_site": current_site, "pages": pages},
        content_type="application/xml",
    )

