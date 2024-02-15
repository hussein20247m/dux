from django.shortcuts import render, get_object_or_404 , redirect
from django.views.generic import ListView, DetailView
from .models import Quiz, Question, MCQuestion, Choice
import datetime
from lectures.models import subtopicsLecturecontain ,Lecture
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

def QuizListView(request):
    lecture = Lecture.objects.all()
    lecture_title = subtopicsLecturecontain.objects.all()
    quizzes = Quiz.objects.all()

    return render(request , 'backend/quiz/quiz_list.html' ,{'lecture':lecture, 'lecture_title' : lecture_title , 'quizzes':quizzes})


def view_lecture_titles(request):
    lecture_id = request.GET.get('lecture_id')
    
    # Retrieve titles based on the selected lecture_id
    titles = subtopicsLecturecontain.objects.filter(lecture_id=lecture_id)

    # Create HTML options for the dropdown
    options = ''.join([f'<option value="{title.pk}">{title.title}</option>' for title in titles])

    # Return JSON response with HTML options
    return JsonResponse({'options': options})



    


def QuizAdd(request):
    lecture = Lecture.objects.all()
    lecture_title = subtopicsLecturecontain.objects.all()


    if request.method == 'POST':
        course = request.POST.get('lecture_title')
        course_s = subtopicsLecturecontain.objects.get( pk=course)
        print('-------------------------------------------\n\n\n')
        print(course)
        title= request.POST.get('title_quiz')
        category= request.POST.get('category_chosse')
        pass_mark= request.POST.get('number')
        timestamp = datetime.datetime.now()

        Q = Quiz(course = course_s  , title= title , category = category ,pass_mark=pass_mark , timestamp = timestamp)
        Q.save()
        return redirect('quiz:quiz.list')
    return render(request , 'backend/quiz/quiz_add.html' ,{'lecture' : lecture , 'lecture_title':lecture_title})



def get_lecture_titles(request):
    lecture_id = request.GET.get('lecture_id')
    
    # Retrieve titles based on the selected lecture_id
    titles = subtopicsLecturecontain.objects.filter(lecture_id=lecture_id)

    # Create HTML options for the dropdown
    options = ''.join([f'<option value="{title.pk}">{title.title}</option>' for title in titles])

    # Return JSON response with HTML options
    return JsonResponse({'options': options})





def template(question_id):
    template = """Give me 2 MCQs and one free response question related to: {doc}"""
    PROMPT_Question = PromptTemplate(
    input_variables=["doc"], template=template, 
    )
    model = OpenAI()

    chain = LLMChain(llm=model, prompt=PROMPT_Question)
    question_g = chain.run({'doc': question_id})

    return question_g





def QuizDetailView(request):
    quiz = Quiz.objects.all()
   
    if request.method == 'POST' :
        lecture = request.POST.get('lecture')
        lecture_title = request.POST.get('lecture_title')
        question_id = Quiz.objects.get(course__pk=lecture_title)
        question_g = template(question_id)
        questions_list = [q.strip() for q in question_g.split('\n') if q]

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
        return render(request , 'backend/quiz/quiz_detail.html' ,{'question':question_id })

    return render(request , 'backend/quiz/quiz_detail.html' ,{'quiz':quiz})

def get_question(request):
    lecture_id = request.GET.get('lecture_id')
    # Retrieve titles based on the selected lecture_id
    titles = Question.objects.get(pk=lecture_id)
    mCQuestion = Choice.objects.filter(question_id__pk=titles)


    # Create HTML options for the dropdown
    options = ''.join([f'<option value="{title.pk}">{title} - {title.correct}</option>' for title in mCQuestion])

    # Return JSON response with HTML options
    return JsonResponse({'options': options})


def QuestionDetailView(request , pk):
    question = Question.objects.filter(pk=pk)
    question_M = MCQuestion.objects.get(pk=pk)
    mCQuestion = Choice.objects.filter(question_id__pk=pk)

    return render(request , 'backend/quiz/question_detail.html' ,{'question':question ,'question_M':question_M ,'mCQuestion':mCQuestion})


def quizadd(request) :


    return render(request , 'backend/quiz/quiz_add.html')