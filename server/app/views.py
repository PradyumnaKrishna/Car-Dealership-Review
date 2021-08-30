from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse

from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request


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
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"{settings.CF_API_ENDPOINT}/review"

        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)

        review_names = ' '.join([review.sentiment for review in reviews])
        return HttpResponse(review_names)


def add_review(request, dealer_id):
    if request.user.is_authenticated and request.method == "POST":
        url = f"{settings.CF_API_ENDPOINT}/review"
        review = dict()
        review["id"] = request.POST("id")
        review["time"] = request.POST("time")
        review["name"] = request.POST("name")
        review["dealership"] = dealer_id
        review["review"] = request.POST("review")
        review["purchase"] = request.POST("purchase")
        review["purchase_date"] = request.POST("purchase_date")
        review["car_make"] = request.POST("car_make")
        review["car_model"] = request.POST("car_model")
        review["car_year"] = request.POST("car_year")

        json_payload = {review: review}
        response = post_request(url, json_payload)

        return HttpResponse(str(response))
