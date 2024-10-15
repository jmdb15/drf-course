from django.urls import path, include

from .views import BookListView, BookCreateView


urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('create/', BookCreateView.as_view(), name='create-book'),
]
