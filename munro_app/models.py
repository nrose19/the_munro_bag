from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

#user attributes -- django auth will handle userName, email, passwordHash
#max_length only for text. not InterField
#django auto creatse PK for every model

# Create your models here.

class Munro(models.Model):
    name = models.CharField(max_length=200)
    height = models.IntegerField(help_text = "Metres")

    #optional for now/for database
    location = models.CharField(
                                max_length=200, 
                                null = True, 
                                blank =True)
    region = models.CharField(max_length=100)

    #made it so it CAN ONLY BE 1-5 
    #optional for now/for database
    difficulty_rating = models.IntegerField(
        help_text = "1 - 5",
        validators = [MinValueValidator (1),
        MaxValueValidator(5)], 
        null = True, 
        blank =True) 

    #optional for now/for database
    description = models.TextField(null = True, blank=True)
    image = models.ImageField(upload_to='munro_images/', null = True, blank=True)

    #optional
    estimated_time_hours = models.DecimalField(
        max_digits = 4, 
        decimal_places = 2, 
        null = True, 
        blank =True)
    #add both blank = True(for form/django level) and null = true(for database level)

    def __str__(self):
        return self.name



class ClimbRecord(models.Model):
    # database -> FK stored like integer
    #integer in ERD but it behaves like onbject in python, 

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name= "climb_records",) 
    
    munro = models.ForeignKey(
        Munro, 
        on_delete =models.CASCADE,
        related_name= "climb_records",) 
    
    climb_date = models.DateField()
    total_meters_climbed = models.IntegerField()
    total_distance = models.IntegerField(help_text = "Kilometres")
    
    # time stored in hours as per current migrations
    completion_time_hours = models.IntegerField()

    #again, enforcing the 1-5 range only
    star_rating = models.IntegerField(
        help_text = "1 - 5",
        validators = [MinValueValidator (1),
        MaxValueValidator(5)],)

    #auto_now_add=True -> timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    #optional
    comments = models.TextField(null = True, blank =True)

    def __str__(self):
        return f"{self.user} - {self.munro} (Climb Date: {self.climb_date})"


class Photo(models.Model):
    record = models.ForeignKey(
        ClimbRecord, 
        on_delete=models.CASCADE,
        related_name= "photos",)
    #each photo belongs to ONE ClimbRecord, One ClimbRecord can have many photos (one to many)
    #photo.record -> gets ClimbRecord...(2 direction of access)
    #record.photo_set.all() -> gives ALL photos attacked to that climb (reverse access)
        #Model name = Photo
        #reverse accessor = photo_set
        #ClimbRecord 1 = Me climbing Ben NEvis and I upload 3 photos
            # photo1, photo2, photo3 but recordID = 1 for all
    #since not using (related_name = "photo").. must write --record.photo_set.all()--

    image = models.ImageField(upload_to='climb_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo(s): {self.record_id}"


class UserFavouriteMunro(models.Model):
    user =models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name= "favourite_munro")
    munro = models.ForeignKey(
        Munro,
        on_delete=models.CASCADE,
        related_name= "favourite_by")
    set_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s favourite Munro: {self.munro}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"
