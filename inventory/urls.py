from django.urls import path, include

from .views import book, borrowlog as blog


urlpatterns = [
    #Book Views
    path('books/', book.BookListView.as_view(), name='home'),
    path('books/create/', book.BookCreateView.as_view(), name='create-book'),
    path('books/<int:pk>/view', book.BookDetailView.as_view(), name='detail-book'),
    path('books/<int:pk>/update', book.BookUpdateView.as_view(), name='update-book'),
    path('books/<int:pk>/delete', book.BookDeleteView.as_view(), name='delete-book'),

    # Borrow Log Views
    path('blog/', blog.BorrowLogListView.as_view(), name='home'),
    path('blog/create/', blog.BorrowLogCreateView.as_view(), name='create-borrow-log'),
    path('blog/<int:pk>/view', blog.BorrowLogDetailView.as_view(), name='detail-borrow-log'),
    path('blog/<int:pk>/update', blog.BorrowLogUpdateView.as_view(), name='update-borrow-log'),
    path('blog/<int:pk>/delete', blog.BorrowLogDeleteView.as_view(), name='delete-borrow-log'),
]
