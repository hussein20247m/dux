from django.shortcuts import render ,redirect
from .models import Course
# Create your views here.
from django.core.files.storage import FileSystemStorage
from .models import User
import datetime
def courses_view(request):
    courses = Course.objects.all()
    return render(request, 'backend/doctor/courses/courses.html' ,{'courses' : courses})

def courses_add(request):
    now = datetime.datetime.now()

    if request.method == 'POST' :
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        #department = request.POST.get('newstitle')
        image = request.POST.get('image')
        #instructor = request.POST.get('newstitle')
        instructor1 = request.POST.get('instructor')
        instructor = User.objects.get(pk =instructor1)
        #last_update = request.POST.get('newstitle')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        course_semester = request.POST.get('course_semester')
        languages = request.POST.get('languages')


        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name , myfile)

        b = Course(name=name ,code=code,description=description,department='-',image=filename,
                instructor=instructor , last_update=now ,status=status ,start_date=start_date,end_date=end_date,
                course_semester=course_semester ,languages=languages)
        b.save()
        return redirect('courses.view')
    return render(request, 'backend/doctor/courses/add_courses.html')


def courses_delete(request , pk) :
    b = Course.objects.get(pk=pk)
    b.image.delete()
    b.delete()
   
    return redirect('courses.view')
