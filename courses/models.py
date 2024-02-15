from django.db import models
from role.models import User


class status(models.TextChoices):
    Inactive = '0'
    Active = '1'
 
class Languages(models.TextChoices):
    English = 'English'
    Turkish = 'Turkish'
# Create your models here.
class Course(models.Model):



    course_semester_choices = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField()
    department = models.CharField(max_length=2, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=status.choices,
        default=status.Inactive
        )
    start_date = models.DateField()
    end_date = models.DateField()
    course_semester = models.CharField(max_length=10, choices=course_semester_choices, default='Spring')
    languages = models.CharField(
        max_length=10,
        choices=Languages.choices,
        default=Languages.English
        )
    def __str__(self):
        return self.name