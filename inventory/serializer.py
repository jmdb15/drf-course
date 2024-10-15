from rest_framework import serializers
from .models import Book, BorrowLog

class BookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Book
        fields = '__all__'
        
class BorrowLog(serializers.ModelSerializer):
    class Meta:
        model = BorrowLog
        fields = '__all__'