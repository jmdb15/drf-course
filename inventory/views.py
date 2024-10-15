from rest_framework import generics
from rest_framework.response import Response

from .models import Book, BorrowLog
from .serializer import BookSerializer, BorrowLog

# Create your views here.
class PaginatedBookListView(ListView):
    model = Book
    
    context_object_name = 'books'
    
    # Default items per page
    paginate_by = 10

    def get_paginate_by(self, queryset):
        # Allow overriding of the pagination limit through query parameters
        return self.request.GET.get('limit', self.paginate_by)