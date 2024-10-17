from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login, RegisterStudentView, DashboardView, ListBooksView, BorrowBookView, ListPendingBooksView, ReturnBookView

# Create a router and register the BookViewSet with it
# router = DefaultRouter()
# router.register(r'books', BookViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # Login-Signup
    path('login/', login, name="login"),
    path('register/', RegisterStudentView.as_view(), name="reg"),
    # WEEK 3
    path('student/my-books', DashboardView.as_view(), name="dashboard"),
    path('student/list-books', ListBooksView.as_view(), name="list-books"),
    path('student/borrow-book', BorrowBookView.as_view(), name="borrow-book"),
    path('student/list-pending-books', ListPendingBooksView.as_view(), name="list-pending"),
    path('student/<int:pk>/return-book', ReturnBookView.as_view(), name="return-book"),
]
