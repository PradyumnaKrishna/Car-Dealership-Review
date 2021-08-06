from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect


def index(request):
    """ index view """
    return render(request, template_name="app/index.html")


def about(request):
    """ contact view """
    return render(request, template_name="app/about.html")


def contact(request):
    """ contact view """
    return render(request, template_name="app/contact.html")


def signup(request):
    """ user signup view """
    context = {}
    if request.method == 'GET':
        return render(request, 'app/user_signup.html', context)

    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        existing_user = User.objects.filter(username=username).first()

        if not existing_user:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            login(request, user)
            return redirect("app:index")

        context['message'] = "User already exists."
        return render(request, 'app/user_signup.html', context)

    return Http404


def login_view(request):
    """ user login view """
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('app:index')

        context['message'] = "Invalid username or password."
        return render(request, 'app/user_login.html', context)

    return render(request, 'app/user_login.html', context)


def logout_view(request):
    """ user logout view """
    logout(request)
    return redirect('app:index')
