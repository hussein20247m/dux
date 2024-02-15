from django import forms
from .models import Grades, QuestionGrade ,TotalGrades
from django.db import  transaction

class GradesAdminForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['user_id', 'course_id', 'lecture_id', 'subtopic_id', 'quiz_id' ,'question_grades']

    question_grades = forms.ModelMultipleChoiceField(
        queryset=QuestionGrade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)

        with transaction.atomic():
            instance.save()

            TotalGrades.calculate_total_grades(instance.user_id, instance.course_id)

            instance.question_grades.set(self.cleaned_data['question_grades'])

        return instance