from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile = request.user.profile
    context = {'profile': profile}


    if hasattr(profile, "is_teacher") and profile.is_teacher:
        return render(request, 'teacher/profile.html', context)
    elif hasattr(profile, "is_student") and profile.is_student:
        return render(request, 'student/profile.html', context)
    else:
        return render(request, 'common_data/profile.html', context)

def login_handler(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "registration/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "registration/login.html")


def logout_handler(request):
    logout(request)
    return redirect("login")

def register_handler(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        if password != confirm_password:
            return render(request, 'registration/register.html', {
                'error': 'Passwords do not match'
            })


        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {
                'error': 'Username already exists'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html', {
                'error': 'Email already exists'
            })


        new_user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )


        login(request, new_user)
        return redirect('home')

    return render(request, 'registration/register.html')
