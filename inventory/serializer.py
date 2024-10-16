from rest_framework import serializers
from .models import Book, BorrowLog
from base.serializers import StudentSerializer
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta: 
        model = Book
        fields = '__all__'

    def get_message(self, obj):
        blog = BorrowLog.objects.get(book=obj)
        if timezone.now().date() > blog.due_date:
            return "This book is already past due to the date of return."
        return None

    def validate_title(self, value):
        if Book.objects.filter(name=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def validate_date_published(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value
        
class BorrowLogSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    # book = BookSerializer()
    # student = serializers.CharField(source="student.username", default=None)

    class Meta:
        model = BorrowLog
        fields = '__all__'

    # def get_student(self, obj:BorrowLog):
    #     return obj.student.first_name


    