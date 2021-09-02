from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse

from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel

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


def get_dealerships(request):
    if request.method == "GET":
        url = f"{settings.CF_API_ENDPOINT}/dealership"

        context = dict()
        context["dealership_list"] = get_dealers_from_cf(url)

        return render(request, 'app/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"{settings.CF_API_ENDPOINT}/review"

        context = dict()
        context["review_list"] = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["dealer_id"] = dealer_id

        return render(request, 'app/dealer_details.html', context)


def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            url = f"{settings.CF_API_ENDPOINT}/review"
            car = CarModel.objects.get(id=request.POST.get('car'))

            review = dict()
            review["dealership"] = dealer_id
            review["review"] = request.POST["review"]
            review["purchase"] = True if request.POST["purchase"] is "on" else False
            review["purchase_date"] = request.POST["purchase_date"]
            review["id"] = request.user.id
            review["name"] = request.user.username
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.year

            json_payload = dict()
            json_payload["review"] = review
            json = post_request(url, json_payload)
            print(json)

            return redirect('app:dealer_details', dealer_id)

        if request.method == "GET":
            context = dict()
            context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
            context["dealer_id"] = dealer_id

            return render(request, 'app/add_review.html', context)

    return redirect('app:index')