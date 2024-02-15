from django.contrib import admin

from .models import Lecture ,subtopicsLecturecontain ,LessonTitle
# Register your models here.



admin.site.register(Lecture)
admin.site.register(LessonTitle)

admin.site.register(subtopicsLecturecontain)

