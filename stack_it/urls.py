from django.urls import path, include
from stack_it.views import StackItView

app_name = 'stack_it'
urlpatterns = [
    path('', StackItView.as_view()),
    path('<path:path>', StackItView.as_view())
]
