from django.contrib import admin
from .models import Book, BorrowLog

# Register your models here.

admin.site.register(Book)
admin.site.register(BorrowLog)