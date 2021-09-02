from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('about', views.about, name="about"),
    path('contact', views.contact, name="about"),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.signup, name='signup'),

    path('', views.get_dealerships, name='index'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:dealer_id>/review/', view=views.add_review, name="add_review"),
]