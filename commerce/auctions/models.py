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
    

'''
Models: Your application should have at least three models in addition to the User model: 
one for auction listings, one for bids, and one for comments made on auction listings. 
Its up to you to decide what fields each model should have, and what the types of those fields should be. 
You may have additional models if you would like.
'''