from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login

# Create a router and register the BookViewSet with it
# router = DefaultRouter()
# router.register(r'books', BookViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', login, name="login"),
]
