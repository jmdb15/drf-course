from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import Student
from inventory.models import BorrowLog

class StudentSerializer(serializers.ModelSerializer):
    borrowed_count = serializers.SerializerMethodField("get_asd")

    class Meta: 
        model = Student
        fields = '__all__'
    
    def get_asd(self, obj:BorrowLog):
        return BorrowLog.objects.filter(student=obj).count()
    

class StudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Student
        fields = ['username', 'password', 'email']
    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.is_superuser = False
        student.is_staff = False
        student.save() 

        group, created = Group.objects.get_or_create(name='Student')  
        student.groups.add(group) 

        return student