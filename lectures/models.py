from django.db import models
from courses.models import Course
from role.models import User



class LessonTitle(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}  "

    
class Lecture(models.Model):
    titles = models.ManyToManyField(LessonTitle)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE )


    def __str__(self): 
        return f"{self.course.name} - {self.instructor}"



class subtopicsLecturecontain(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE )
    title = models.ForeignKey(LessonTitle, on_delete=models.CASCADE )
    video_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)
    exam_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.lecture_id.course.name} - {self.title} "