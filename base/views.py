import requests, os

from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from .models import Student
from inventory.models import Book, BorrowLog
from inventory.serializers import BookSerializer, MyBooksSerializer
from inventory.pagination import Paginate10
from inventory.permissions import IsOwner
from .permissions import IsStudent
from .serializers import StudentRegistrationSerializer
from inventory.serializers import BorrowLogSerializer

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
    queryset = Student.objects.all()
    serializer_class = StudentRegistrationSerializer
    

# WEEK 3
class DashboardView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = MyBooksSerializer
    pagination_class = Paginate10
    permission_classes = [IsAuthenticated, IsStudent]

    def list(self, request, *args, **kwargs):
        logs = BorrowLog.objects.filter(student__id=request.user.id)
        referenced_books = [log.book for log in logs] 
        unique_books = list(set(referenced_books))
        serializer = self.get_serializer(unique_books, many=True)
        return Response(serializer.data)

class ListBooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class BorrowBookView(generics.CreateAPIView):
    # queryset = BorrowLog.objects.all()
    serializer_class = BorrowLogSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, *args, **kwargs):

        book_id = request.data['book_id']
        due_date = request.data['due_date']
        
        if Book.objects.filter(id=book_id, quantity=0).exists():
            raise serializers.ValidationError(dict({
                "message":"This book is not available for borrowing as the quantity is 0.",
                "hint":"There is no more book to give."
            }))
        if BorrowLog.objects.filter(book__id=book_id, student=request.user).exclude(status='returned').exists():
            raise serializers.ValidationError(dict({
                "message": "You already borrowed this book.",
                "hint":"Clear your request or return the book."
            }))
        book = Book.objects.get(id=book_id)
        try:
            blog = BorrowLog.objects.create(
                book=book,
                student=request.user,
                due_date=due_date 
            )
            return Response(dict({
                "message":"Success"
            }))
        except Exception as e:
            print(e)
            return Response(dict({
                "message":'Something went wrong'
            }))

        # serialized = self.get_serializer()
        # return super().post(request, *args, **kwargs)


class ListPendingBooksView(generics.ListAPIView):
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        pending_logs = BorrowLog.objects.filter(student=request.user, status='pending')
        book_ids = pending_logs.values_list('book', flat=True)
        books = Book.objects.filter(id__in=book_ids)
        serialized_data = self.get_serializer(list(set(books)), many=True)
        return Response(serialized_data.data)

class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowLog.objects.all()
    serializer_class = BorrowLogSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsStudent]

    def update(self, request, *args, **kwargs):
        print(request.user.id)
        request_data = request.data.copy()
        request_data['status'] = 'returned' 
        request_data['date_returned'] = timezone.now() 

        serializer = self.get_serializer(self.get_object(), data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)