from django.db import models
from lectures.models import subtopicsLecturecontain ,Lecture
from django.dispatch import receiver
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator,
    validate_comma_separated_integer_list,
)
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
from django.conf import settings
import re
from django.db.models import Q
from model_utils.managers import InheritanceManager
import json



CATEGORY_OPTIONS = (
    ("assignment", _("Assignment")),
    ("exam", _("Exam")),
    ("quiz", _("Quiz")),
)



class Quiz(models.Model):
    course = models.ForeignKey(subtopicsLecturecontain, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name=_("Title"), max_length=60, blank=False)
    category = models.TextField(choices=CATEGORY_OPTIONS, blank=True)
    pass_mark = models.SmallIntegerField(blank=True,default=50,validators=[MaxValueValidator(100)],)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def get_questions(self):
        return self.question_set.all().select_subclasses()


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz, blank=True)
    content = models.CharField(max_length=1000,blank=False,)
    objects = InheritanceManager()
    def __str__(self):
        return self.content
    

class MCQuestion(Question):
    def check_if_correct(self, guess):
        answer = Choice.objects.get(id=guess)
        if answer.correct is True:
            return True
        else:
            return False

    def get_choices(self):
        return self.order_choices(Choice.objects.filter(question=self))
    def get_choices_list(self):
        return [
            (choice.id, choice.choice)
            for choice in self.order_choices(Choice.objects.filter(question=self))
        ]
    def answer_choice_to_string(self, guess):
        return Choice.objects.get(id=guess).choice


class Choice(models.Model):
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    choice = models.CharField(max_length=1000,blank=False,)
    correct = models.BooleanField(blank=False,default=False,)
    def __str__(self):
        return self.choice


