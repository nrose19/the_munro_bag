from django.db import models
from django.contrib.auth.models import User

#user attributes -- django auth will handle userName, email, passwordHash
#max_length only for text. not InterField
#django auto creatse PK for every model

# Create your models here.

class Munro(models.Model):
    name = models.CharField(max_length=200)
    height = models.IntegerField(help_text = "Metres")
    location = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

#how do i make sure they can't put 6+
    difficulty_rating = models.IntegerField(help_text = "1 - 5") 

    description = models.TextField()
    storage_key =models.CharField(max_length = 512)
    content_type =models.CharField(max_length= 100)

    #optional
    estimated_time_hours = models.DecimalField(
        max_digits = 4, decimal_places = 2, null = True, blank =True)
    #add both blank = True(for form/django level) and null = true(for database level)

    def __str__(self):
        return self.name



class ClimbRecord(models.Model):
    # database -> FK stored like integer
    #integer in ERD but it behaves like onbject in python, 

    user = models.ForeignKey(User, on_delete = models.CASCADE) 
    # (settings.AUTH_USER_MODEL, on_delete = models.CASCADE)...better than import User??
    # would need to use "from django.conf import settings" but look more into it first..dont fully get

    munro = models.ForeignKey(Munro, on_delete =models.CASCADE) 
    climb_date = models.DateField()
    total_meters_climbed = models.IntegerField()
    total_distance = models.IntegerField(help_text = "Kilometres")
    completion_time_minutes = models.IntegerField()
    star_rating = models.IntegerField(help_text= "1 - 5")
    created_at = models.DateTimeField(auto_now_add=True) #aauto_now_add=True -> timestamp

    #optional
    comments = models.TextField(null = True, blank =True)

    def __str__(self):
        return f"{self.user} - {self.munro} (Climb Date: {self.climb_date})"


class Photo(models.Model):
    record = models.ForeignKey(ClimbRecord, on_delete=models.CASCADE)
    #each photo belongs to ONE ClimbRecord, One ClimbRecord can have many photos (one to many)
    #photo.record -> gets ClimbRecord...(2 direction of access)
    #record.photo_set.all() -> gives ALL photos attacked to that climb (reverse access)
        #Model name = Photo
        #reverse accessor = photo_set
        #ClimbRecord 1 = Me climbing Ben NEvis and I upload 3 photos
            # photo1, photo2, photo3 but recordID = 1 for all
    #since not using (related_name = "photo").. must write --record.photo_set.all()--

    #URL/key
    storage_key = models.CharField(max_length= 512)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Photo(s): {self.record_id}"


class UserFavouriteMunro(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    munro = models.ForeignKey(Munro,on_delete=models.CASCADE)
    set_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favourite Munro: {self.munro}"
        # should i add {self.user}??