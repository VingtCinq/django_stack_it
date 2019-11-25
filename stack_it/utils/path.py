from stack_it.models import Page

class PagePathConverter:
    regex = '.+'

    def to_python(self, path):
        return path

    def to_url(self, page):
        return Page.objects.get(key=page).ref_full_path[1:]



