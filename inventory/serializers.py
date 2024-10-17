from rest_framework import serializers
from .models import Book, BorrowLog
from base.serializers import StudentSerializer
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Book
        fields = ['id', 'title','code', 'cover_image', 'author', 'date_published', 'quantity']

    def validate_title(self, value):
        if Book.objects.filter(title=value).exists():
            raise serializers.ValidationError("This name already exists.")
        return value

    def validate_date_published(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value
        

class MyBooksSerializer(BookSerializer):
    message = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['message']

    def get_message(self, obj):
        try:
            blog = BorrowLog.objects.get(book=obj)
            if timezone.now().date() > blog.due_date:
                return "This book is already past due to the date of return."
        except:
            pass 
        return None

class BorrowLogSerializer(serializers.ModelSerializer):
    # student = StudentSerializer()
    # book = BookSerializer()
    # student = serializers.CharField(source="student.username", default=None)

    class Meta:
        model = BorrowLog
        fields = '__all__'

    # def create(self, validated_data):
    #     book_id = validated_data.pop('book_id', None) 
    #     book = Book.objects.get(id=book_id) 
    #     student = self.context['request'].user  
    #     borrow_log = BorrowLog.objects.create(
    #         book=book,
    #         student=student,
    #         **validated_data  
    #     )
    #     return borrow_log


    