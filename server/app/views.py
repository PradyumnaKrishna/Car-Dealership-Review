from django.shortcuts import render


def index(request):
    return render(request, template_name="app/index.html")


def about(request):
    return render(request, template_name="app/about.html")


def contact(request):
    return render(request, template_name="app/contact.html")
