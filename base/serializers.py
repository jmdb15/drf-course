from rest_framework import serializers

from .models import Student
from inventory.models import BorrowLog

class StudentSerializer(serializers.ModelSerializer):
    borrowed_count = serializers.SerializerMethodField("get_asd")

    class Meta: 
        model = Student
        fields = '__all__'
    
    def get_asd(self, obj:BorrowLog):
        return BorrowLog.objects.filter(student=obj).count()