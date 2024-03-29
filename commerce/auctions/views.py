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
        
        #create new bid object
        new_bid = Bid(
            bid = float(price),
            user = current_user
        )
        new_bid.save()
        
        #create new listing object
        new_listing = Listing(
            title = title,
            description = description,
            image_url = image_url,
            price = new_bid,
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

def listing_list(request, category_id):
    from django.shortcuts import get_object_or_404
    category = get_object_or_404(Category, pk=category_id)
    
    # use a reverse lookup on listings_category foreign key name
    listings = category.listings_category.all()
    return render(request, "auctions/select_category.html", {
        "listings" : listings,
        "category" : category,
    })
    
def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    in_watch_list = request.user in listingData.watch_list.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing" : listingData,
        "in_watch_list" : in_watch_list,
        "comments" : allComments
    })
    
def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watch_list.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watch_list.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchList(request):
    currentUser = request.user
    list = currentUser.listingWatchList.all()
    return render(request, "auctions/watchList.html", {
        "list" : list
    })
    
def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    
    newComment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )
    
    newComment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    in_watch_list = request.user in listingData.watch_list.all()
    allComments = Comment.objects.filter(listing=listingData)
    
    if float(newBid) > listingData.price.bid:
        updateBid = Bid(
            user = request.user,
            bid=float(newBid)
        )
        updateBid.save()
        
        listingData.price = updateBid
        listingData.save()
        
        return render(request, "auctions/listing.html", {
            "listing" : listingData,
            "message": "Successful Bid",
            "update" : True,
            "in_watch_list" : in_watch_list,
            "comments" : allComments
        })
    
    else:
        return render(request, "auctions/listing.html", {
            "listing" : listingData,
            "message": "Failed Bid, please place a bid higher than the current price.",
            "update" : False,
            "in_watch_list" : in_watch_list,
            "comments" : allComments
        })