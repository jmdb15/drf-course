from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status

from ..permissions import IsLibrarian
from ..models import Book
from ..serializers import BookSerializer
from ..pagination import Paginate10

# Create your views here.
class BookListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [ IsAuthenticated, IsLibrarian]
  pagination_class = Paginate10


class BookDetailView(generics.RetrieveAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsAuthenticated, IsLibrarian]


class BookCreateView(generics.CreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [IsLibrarian]

  # def post(self, request, *args, **kwargs):
  #   serializer = self.get_serializer(data=request.data)
  #   if serializer.is_valid():
  #       serializer.save()
  #       return response.Response(serializer.data, status=status.HTTP_201_CREATED)
  #   else:
  #       return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BookUpdateView(generics.UpdateAPIView):
   queryset = Book.objects.all()
   serializer_class = BookSerializer
   permission_classes = [IsLibrarian]


class BookDeleteView(generics.DestroyAPIView):
   queryset = Book.objects.all()
  #  serializer_class = BookSerializer