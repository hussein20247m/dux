from django.shortcuts import render , redirect
from .models import Grades  ,QuestionGrade ,TotalGrades
# Create your views here.
from role.models import User
from courses.models import Course 
from lectures.models import Lecture , subtopicsLecturecontain
from quiz.models import Quiz ,Question , Choice
def sunbmit_grades(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        Lecture_id = request.POST.get('Lecture_id')
        course_id = request.POST.get('course_id')
        quiz_id = request.POST.get('quiz_id')
        Question1 = request.POST.get('question1')
        Question2 = request.POST.get('question2')
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')

        subtopics = request.POST.get('subtopics')
        question1 = Question.objects.get(pk=Question1)
        mCQuestion = Choice.objects.filter(question_id__pk=question1.pk)

        question2 = Question.objects.get(pk=Question2)
        mCQuestion2 = Choice.objects.filter(question_id__pk=question2.pk)
        quiz_Mid = Quiz.objects.get(title = '9. Mid Term Exam')
        quiz_Final = Quiz.objects.get(title = '14. Final Exam')

        print(quiz_Mid)
        print(quiz_Final)
        correct111 = ''
        for i in mCQuestion :

            if i.correct :
                correct111 = i.choice
        
        correct222 = ''
        for i in mCQuestion2 :

            if i.correct :
                correct222 = i.choice
        
        
        grade_correct1 = 0
        grade_correct2 = 0

        if answer1 ==  correct111 :
            if quiz_Mid != None:
                grade_correct1 +=40
            elif quiz_Final != None:
                grade_correct1 +=60
            else :
                grade_correct1 +=5

        if answer2 ==  correct222 :
            grade_correct2 +=5


        user_id = User.objects.get(pk =user_id)
        course_id = Course.objects.get(pk =course_id)
        Lecture_id = Lecture.objects.get(pk =Lecture_id)
        subtopics = subtopicsLecturecontain.objects.get(pk =subtopics)
        quiz_id = Quiz.objects.get(pk =quiz_id)

        new1 = Grades(user_id=user_id, course_id=course_id, lecture_id=Lecture_id, subtopic_id=subtopics, quiz_id=quiz_id)
        new2 = Grades(user_id=user_id, course_id=course_id, lecture_id=Lecture_id, subtopic_id=subtopics, quiz_id=quiz_id)

        # Save the Grades instances without adding question_grades initially
        new1.save()
        new2.save()

        # Retrieve the Question instances based on the primary keys
        question1 = Question.objects.get(pk=Question1)
        question2 = Question.objects.get(pk=Question2)

        # Create QuestionGrade instances and add them to the many-to-many field
        question_grade1 = QuestionGrade.objects.create(question_id=question1, grades_question=grade_correct1)
        question_grade2 = QuestionGrade.objects.create(question_id=question2, grades_question=grade_correct2)

        new1.question_grades.set([question_grade1])
        new2.question_grades.set([question_grade2])
        total_instance, created = TotalGrades.objects.get_or_create(user_id=user_id, course_id=course_id)

        total_instance.calculate_total_grades(user_id, course_id, grade_correct1, grade_correct2)
        
        print( 'grade_correct1 ,grade_correct2' ,grade_correct1 ,grade_correct2) 

        return redirect('user.my.courses')