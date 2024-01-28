from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=250)
    image_url = models.CharField(max_length=500)
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listings_category")
    categories = models.ManyToManyField(Category, blank=True, related_name="select_category")
    watch_list = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchList")
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.author} comments on {self.listing}: {self.message}"