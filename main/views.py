from django.shortcuts import render , redirect ,get_object_or_404 
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
from role.models import User 
from courses.models import Course
from lectures.models import Lecture ,subtopicsLecturecontain
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain
from langchain.output_parsers.regex import RegexParser
import os
from quiz.views import template
from quiz.models import MCQuestion ,Choice ,Quiz , Question
from django.core.serializers import serialize
import json

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

# Create your views here.
def home(request) :

    return render(request , 'frontend/index.html' )

def user_login(request) :

    return render(request , 'frontend/login.html' )


def user_register(request) :

    return render(request , 'frontend/register.html' )


def user_dashboard(request) :

    return render(request , 'frontend/dashboard.html' )

def user_profile(request) :

    return render(request , 'frontend/user_profile.html' )



def user_my_courses(request) :
    courses = Course.objects.all()
    return render(request , 'frontend/my_courses.html' ,{'courses':courses})


def user_courses_details(request , pk ) :
        
    courses = Course.objects.get(pk=pk)
    subtopicsall = subtopicsLecturecontain.objects.filter(lecture_id__course__pk=pk)
    request.session['course_id'] = courses.pk
    request.session['subtopicsall'] = list(subtopicsall.values()) 

    return render(request, 'frontend/courses_details.html', {'courses':courses , 'lesson_title' :subtopicsall})




def Generate_questions(request , pk ) :
    titles = subtopicsLecturecontain.objects.get(pk=pk)
    question_id = Quiz.objects.get(course__pk=titles.pk)
    # Retrieve titles based on the selected lecture_id
    Generate_questions = template(titles.title)
    # Create HTML options for the dropdown
    questions_list = [q.strip() for q in Generate_questions.split('\n') if q]

    questions = []
    choices = []
    answers = []

    for item in questions_list:
        if item.startswith('Question'):
            questions.append(item)
        elif item.startswith('CHOICE'):
            choices.append(item.split(':')[-1].strip())
        elif item.startswith('Answer'):
            answers.append(item.split(':')[-1].strip())
    list_pk = []
    for i in range(len(questions)):
        question_instance = MCQuestion.objects.create(content=questions[i])
        question_instance.quiz.add(question_id)
        
        correct_choice_index = ord(answers[i]) - ord('A')
        choices_per_question = len(choices) // len(questions)

        # Create choices for each question
        for j in range(4):

            choice = Choice.objects.create(
                question=question_instance,
                choice=choices[i * choices_per_question + j],
                correct= (j == correct_choice_index)
            )
            choice.save()
        question_instance.save()
        list_pk.append(question_instance.pk)
    
    question1 = Question.objects.get(pk=list_pk[0])
    question2 = Question.objects.get(pk=list_pk[1])
    mCQuestion1 = Choice.objects.filter(question_id__pk=list_pk[0])
    mCQuestion2 = Choice.objects.filter(question_id__pk=list_pk[1])

    Lecture_id = Lecture.objects.get(titles = titles.title).pk

    course_id = Lecture.objects.get(pk=Lecture_id).course.pk

    quiz_id = question_id.pk
    return render(request , 'frontend/quiz/Generate_questions.html' ,{'question1':question1 ,'question2':question2 ,'mCQuestion1':mCQuestion1 ,'mCQuestion2':mCQuestion2 ,  'Lecture_id':Lecture_id , 'course_id':course_id ,'quiz_id':quiz_id , 'subtopics' : titles.pk})




def chatbot(request):
    course_id = request.session.get('course_id')
    subtopicsall = request.session.get('subtopicsall', [])
    thread =[]
    if request.method == 'POST':

        chatbot_input = request.POST.get('chatbot')
        thread.append("You: "+chatbot_input)
        prompt = f"User: {chatbot_input}\nChatbot:"
        chatbot_response = chat_with_gpt3(prompt , subtopicsall)
        thread.append("Chatbot: "+chatbot_response)
    
        return JsonResponse({'thread': thread})

    return render(request , 'frontend/courses_details.html' ,{'thread': thread ,'subtopicsall':subtopicsall ,'course_id':course_id} )
def chat_with_gpt3(prompt ,subtopicsall):
    template = """"I want to answer this question {prompt} related with {subtopicsall} """
    model = OpenAI()
    PROMPT = PromptTemplate(
            input_variables=[], template=template 
        ) 
    chain = LLMChain(llm=model, prompt=PROMPT)
    subtopics = chain.run({"prompt" :prompt ,"subtopicsall" :subtopicsall})

    return subtopics

def admin_profile_update(request , pk):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        Address = request.POST.get("Address")
        b = User.objects.get(pk =pk)
 
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        
        b.image.delete()

        b.full_name = full_name
        b.phone_number = phone_number
        b.Address = Address
        b.image =filename

        b.save()

        return redirect('super.profile')




def edit_users_manager(request , pk) :
    users_edit = User.objects.get(pk=pk)
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        Email = request.POST.get('Email')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status')
        Role = request.POST.get('Role')
        Address = request.POST.get('Address')
         
        myfile = request.FILES['image']
        fs = FileSystemStorage(location='users/')
        filename = fs.save(myfile.name , myfile)


        users_updete = User.objects.get(pk=pk)
        users_updete.full_name =full_name
        users_updete.username =username
        users_updete.Email =Email
        users_updete.phone_number =phone_number
        users_updete.status =status
        users_updete.Role =Role
        users_updete.Address =Address
        users_updete.filename =filename
        users_updete.save()

        return redirect('super.view.admin')
    return render(request , 'backend/admin/users/edit_users.html' , {'users_edit':users_edit})



def user_view_admin(request) :
    userall = User.objects.all()

    return render(request , 'backend/admin/users/user_view.html' ,{'userall': userall})


def doctor_view_admin(request) :
    userall = User.objects.all()

    return render(request , 'backend/admin/users/doctor_view.html' ,{'userall': userall})



def admin_view_admin(request) :
    userall = User.objects.all()

    return render(request , 'backend/admin/users/admin_view.html' ,{'userall': userall})




def doctor_profile_update(request , pk):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        Address = request.POST.get("Address")
        b = User.objects.get(pk =pk)
        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)             
        b.image.delete()
        b.full_name = full_name
        b.phone_number = phone_number
        b.Address = Address
        b.image =filename
        b.save()

        return redirect('doctor.profile')
    

def user_profile_update(request , pk):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        Address = request.POST.get("Address")
        b = User.objects.get(pk =pk)
        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        
        
        b.image.delete()


        b.full_name = full_name
        b.phone_number = phone_number
        b.Address = Address
        b.image =filename
        b.save()

        return redirect('user.profile')

def doctor_dashboard(request) :
    return render(request , 'backend/doctor/index.html' )

def doctor_profile(request) :
    return render(request , 'backend/doctor/profile.html' )



def return_to_dashboard_admin(request):
    return redirect(super.dashboard)


def is_admin(user):
    return user.is_authenticated and user.Role == 'is_admin'

def is_doctor(user):
    return user.is_authenticated and user.Role == 'is_doctor'or user.Role == 'is_admin'

def is_student(user):
    return user.is_authenticated and user.Role == 'is_student' or  user.Role == 'is_doctor'or user.Role == 'is_admin'




def admin_dashboard(request) :
    return render(request , 'backend/admin/index.html' )

def admin_profile(request) :
    return render(request , 'backend/admin/profile.html' )





