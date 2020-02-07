from django.urls import path

from .views import BasicView, CustomView, HomeView

urlpatterns = [
    path('', BasicView.as_view()),
    path('customapi', CustomView.as_view()),
    path('search_result', HomeView.as_view())
]
