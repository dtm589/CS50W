from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    all_listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings" : all_listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        #get the data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        category = request.POST["category"]
        current_user = request.user
        
        #get specific category
        category_data = Category.objects.get(category_name=category)
        
        #create new listing object
        new_listing = Listing(
            title = title,
            description = description,
            image_url = image_url,
            price = float(price),
            category = category_data,
            owner = current_user
        )
        
        #add to database here
        new_listing.save()
        
        #redirect to new listing NEED TO FIX
        return HttpResponseRedirect(reverse("index"))
    
    else:
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "category" : all_categories
        })
        
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "category" : all_categories
    })

def select_category(request, category):
    all_listing = Listing.objects.filter(category=category)
    return render(request, "auctions/select_category.html", {
        "listings" : all_listing
    })