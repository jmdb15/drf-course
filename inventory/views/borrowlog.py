from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status

from ..permissions import IsLibrarian, IsOwner
from ..models import BorrowLog, Book
from ..serializers import BorrowLogSerializer
from ..pagination import Paginate10

# Create your views here.
class BorrowLogListView(generics.ListAPIView):
  queryset = BorrowLog.objects.all()
  serializer_class = BorrowLogSerializer
  permission_classes = [ IsLibrarian]
  pagination_class = Paginate10


class BorrowLogDetailView(generics.RetrieveAPIView):
  queryset = BorrowLog.objects.all()
  serializer_class = BorrowLogSerializer
  permission_classes = [IsAuthenticated, IsLibrarian]

  def get_object(self):
    return BorrowLog.objects.filter(student__id=2).first()


class BorrowLogCreateView(generics.CreateAPIView):
  # queryset = BorrowLog.objects.all()
  serializer_class = BorrowLogSerializer
  permission_classes = [IsLibrarian]

  # def post(self, request, *args, **kwargs):
  #   serializer = self.get_serializer(data=request.data)
  #   if serializer.is_valid():
  #       serializer.save()
  #       return response.Response(serializer.data, status=status.HTTP_201_CREATED)
  #   else:
  #       return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BorrowLogUpdateView(generics.UpdateAPIView):
   queryset = BorrowLog.objects.all()
   serializer_class = BorrowLogSerializer
   permission_classes = []


class BorrowLogDeleteView(generics.DestroyAPIView):
   queryset = BorrowLog.objects.all()
   permission_classes = [IsOwner]
  #  serializer_class = BorrowLogSerializer