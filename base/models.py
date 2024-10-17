from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Student(AbstractUser):
    pass

    def str(self):
        return f"{self.first_name} {self.last_name}"