from django.db import models
from role.models import User
from courses.models import Course
from lectures.models import Lecture, subtopicsLecturecontain
from quiz.models import Quiz, Question

# Create your models here.

class QuestionGrade(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    grades_question = models.IntegerField()
    def __str__(self): 
        return f"{self.question_id} - {self.grades_question}"

class Grades(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    subtopic_id = models.ForeignKey(subtopicsLecturecontain, on_delete=models.CASCADE, null=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question_grades = models.ManyToManyField(QuestionGrade, blank=True)

    def __str__(self): 
        return f"{self.course_id} - {self.user_id} - {self.lecture_id} - {self.question_grades}"

class TotalGrades(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_grades = models.IntegerField(default=0)

    @classmethod
    def calculate_total_grades(cls, user_id, course_id, *question_grades):
        total_question_grades = sum(question_grades)

        # Save or update the total grades in the TotalGrades model
        total_grade_obj, created = cls.objects.get_or_create(user_id=user_id, course_id=course_id)
        total_grade_obj.total_grades += total_question_grades
        total_grade_obj.save()

        return total_question_grades
    
    def __str__(self): 
        return f"{self.course_id} - {self.user_id}"
