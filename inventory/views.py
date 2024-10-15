from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status

from .permissions import IsLibrarian
from .models import Book, BorrowLog
from .serializer import BookSerializer, BorrowLog

# Create your views here.
# class PaginatedBookListView(ListView):
#     model = Book
    
#     context_object_name = 'books'
    
#     # Default items per page
#     paginate_by = 10

#     def get_paginate_by(self, queryset):
#         # Allow overriding of the pagination limit through query parameters
#         return self.request.GET.get('limit', self.paginate_by)


class BookListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [ IsLibrarian]

class BookDetailView(generics.RetrieveAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsLibrarian]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]

    def post(self, request, *args, **kwargs):
        # Add custom logic before saving the object
        data = request.data
        print(f"Request Data: {data}")  # Example: Logging request data
        
        # Call the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
           return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
