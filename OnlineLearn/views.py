from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

def index(request, message = None):
    return render(request, 'OnlineLearn/home.html')

def login_view(request):
    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "OnlineLearn/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "OnlineLearn/login.html")


def register_view(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "OnlineLearn/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email = email, password = password, first_name = firstname, last_name = lastname)
            user.save()
        except IntegrityError:
            return render(request, "OnlineLearn/register.html", {
                "message": "The mail already registered."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "OnlineLearn/register.html")

def logout_view(request):
    logout(request)
    return index(request, "Logged out Succesfully!")
