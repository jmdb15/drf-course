import requests, os

from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from .models import Student
from inventory.models import Book, BorrowLog
from inventory.serializer import BookSerializer
from inventory.pagination import Paginate10
from .serializers import StudentSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    load_dotenv()
    
    user = request.data.get('username')
    password = request.data.get('password')

    
    token_url = f"{settings.OAUTH2_PROVIDER_URL}/token/"
    client_id = os.environ.get('OAUTH2_CLIENT_ID')
    client_secret = os.environ.get('OAUTH2_CLIENT_SECRET')
    
    print(client_id)
    print(client_secret)

    data = {
        'grant_type' : 'password',
        'client_id' : client_id,
        'client_secret' : client_secret,
        'username' : user,
        'password' : password
    }

    try:
        response = requests.post(token_url, data=data)
        response_data = response.json()

        if response.status_code == 200:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(response_data, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterStudentView(generics.CreateAPIView):
    # queryset = Student.objects.all()
    serializer_class = StudentSerializer
    

# WEEK 3
class DashboardView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = Paginate10
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logs = BorrowLog.objects.filter(student__id=request.user.id)
        referenced_books = [log.book for log in logs] 
        unique_books = list(set(referenced_books))
        serializer = BookSerializer(unique_books, many=True)
        return Response(serializer.data)