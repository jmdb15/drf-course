from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login, RegisterStudentView, DashboardView

# Create a router and register the BookViewSet with it
# router = DefaultRouter()
# router.register(r'books', BookViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # Login-Signup
    path('login/', login, name="login"),
    path('register/', RegisterStudentView.as_view(), name="reg"),
    # dashboard
    path('student/my-books', DashboardView.as_view(), name="dashboard"),
]
