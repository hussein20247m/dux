from django.db import models
from django.contrib.auth.models import AbstractUser

class role(models.TextChoices) :
    is_admin = 'is_admin'
    is_doctor = 'is_doctor'
    is_student = 'is_student'


class status(models.TextChoices):
    Inactive = '0'
    Active = '1'
 



class User(AbstractUser) :
    full_name = models.CharField(max_length=100 ,null=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    phone_number  = models.CharField(max_length=100 ,null=True)
    status = models.CharField(
        max_length=10,
        choices=status.choices,
        default=status.Inactive
        )

    Role = models.CharField(
        max_length =10 ,
        choices = role.choices,
        default = role.is_student
    )
    Address= models.CharField(max_length=100 ,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) :
        return self.username