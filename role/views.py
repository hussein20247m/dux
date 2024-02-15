from django.shortcuts import render ,redirect ,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import User
from .forms import UserRegisterForm
# Create your views here.

def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, 'frontend/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None and user.Role == 'is_admin' :
                login(request, user)
                messages.success(request, "You are logged.")
                return redirect('super.dashboard')
            
            elif user is not None and user.Role == 'is_doctor':
                login(request, user)
                return redirect('doctor.dashboard')
            elif user is not None and user.Role == 'is_student':
                login(request, user)
                return redirect('user.dashboard')
            else:
                messages.warning(request, "Username or password does not exist")
                return render(request, 'frontend/login.html')
            
             
            
        except:
            messages.warning(request, "User does not exist")

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return render(request, 'frontend/login.html')
        
    return render(request, 'frontend/login.html')


def logoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")



