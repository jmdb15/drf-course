from django.db import models

from base.models import Student

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    cover_image = models.ImageField(blank=True, null=True)
    author= models.CharField(max_length=200)
    date_published = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    
class BorrowLog(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('borrowed','Borrowed'),
        ('returned','Returned'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateTimeField(blank=True, null=True)
    date_returned = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    