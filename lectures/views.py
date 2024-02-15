from django.shortcuts import render ,get_object_or_404 , redirect
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.llm import LLMChain

from .models import Lecture ,subtopicsLecturecontain ,LessonTitle
import os
from role.models import User
from courses.models import Course
from django.core.files.storage import FileSystemStorage
from quiz.models import Quiz
import datetime
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# Create your views here.
def lectures_generate(request):
    course = Course.objects.all()
    if request.method == 'POST' :
        
        course_id = request.POST.get("course_id")
        generate = Course.objects.get(pk =course_id).name

        # Simple prompt with placeholders
        template = """"Give me a 14 subtopics for the course with title: {content} . The 9th topic should be Mid Term Exam and the 14th topic should be Final Exam .. Format the response as list of variables
        Example subtopics :

        """
     
        model = OpenAI()
        PROMPT = PromptTemplate(
            input_variables=[], template=template , 
        )
        # Convert the filled prompt to a list of variables
        chain = LLMChain(llm=model, prompt=PROMPT)

        subtopics = chain.run(generate)
        subtopics_list = [item.strip() for item in subtopics.split('\n') if item.strip()]
 
        return render(request , 'backend/doctor/lectures/generate_lectures.html' , {'course_id':course_id ,'subtopics_list':subtopics_list})


    return render(request, 'backend/doctor/lectures/generate_lectures.html' ,{'course':course} )


def save_lectures_generate(request):
    if request.method == 'POST':
        # Assuming you have the course_id and instructor_id available
        course_id = request.POST.get('course_id')
        instructor_id = request.POST.get('instructor')
        # Create a lectures instance


        
        template_video_url =""""I want to generate one url globle YouTube related to the {title} {content} topics and The video consists only of education from Stanford 
        I want to make sure that the link is valid and works well and the video is on YouTube ..The duration of the video should not exceed 5 minutes
        I just want a one link, not an explanation

        """

      
        course_name = Course.objects.get(pk=course_id).name

        model = OpenAI()
        PROMPT = PromptTemplate(
             input_variables=[] ,template=template_video_url ,  
        )
        chain = LLMChain(llm=model, prompt=PROMPT)


        b = Lecture(course_id=course_id, instructor_id=instructor_id)
        b.save()
        titles = [request.POST.get(f'name_{i}') for i in range(1, 15)]
        lesson_titles = [LessonTitle.objects.create(title=title) for title in titles]
        b.titles.set(lesson_titles)

        b.save()

        timestamp = datetime.datetime.now()
        for i in lesson_titles :
            video_url = chain.run({'title':course_name ,'content' : i})
            s = subtopicsLecturecontain(lecture_id=b ,title=i ,video_url=video_url,pdf_file='-' ,exam_link='-')
            s.save()
            Q = Quiz(course = s  , title= i , category = 'quiz' ,pass_mark='50' , timestamp = timestamp)
            Q.save()


    return redirect('courses.view')



def lectures_view(request):
    lectuere = Lecture.objects.all()
    return render(request , 'backend/doctor/lectures/lectures.html' ,{'lectuere':lectuere})




def lectures_delete(request , pk) :
    b = Lecture.objects.get(pk=pk)
    b.delete()
   
    return redirect('lectures.view')


def lectures_edit(request, pk):
    bL = Lecture.objects.filter(pk=pk)


    return render(request, 'backend/doctor/lectures/lectures_edit.html', {'pk': pk, 'b': bL })


def subtitle_edit(request , pkL ,pk ) :
    sub = get_object_or_404(subtopicsLecturecontain, lecture_id=pkL ,title=pk)


    return render(request, 'backend/doctor/lectures/subtitle_edit.html', {'sub': sub })



def subtitle_edit_contain(request, pk):
    if request.method == 'POST':
        b = get_object_or_404(subtopicsLecturecontain, pk=pk)

        title = request.POST.get('title')
        URL = request.POST.get('URL')
        Examlink = request.POST.get('Examlink')

        # Update LessonTitle instance
        lesson_title = LessonTitle.objects.get(pk=b.title.pk)
        lesson_title.title = title
        lesson_title.save()

        myfile = request.FILES['pdfFile']
        fs = FileSystemStorage(location='media/pdf/lecture')
        filename = fs.save(myfile.name , myfile)

        # Update subtopicsLecturecontain instance
        b.title = lesson_title
        b.video_url = URL
        b.pdf_file = filename
        b.exam_link = Examlink
        b.save()

        return redirect('lectures.view')