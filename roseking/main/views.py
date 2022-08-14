from django.shortcuts import render

# Create your views here.


def home(response):
    return render(response, "main/home.html", {})

def gamerules(response):
    return render(response, "main/gamerules.html", {})

def termsofservice(response):
    return render(response, "main/termsofservice.html", {})