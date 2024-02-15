from django.contrib import admin
from .models import Grades , TotalGrades  ,QuestionGrade
# Register your models here.
admin.site.register(Grades)
admin.site.register(TotalGrades)
admin.site.register(QuestionGrade)
