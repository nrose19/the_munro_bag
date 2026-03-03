from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Munro(models.Model):
    name = models.CharField(max_length=200)
    height = models.IntegerField(help_text="Metres")
    location = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    difficulty_rating = models.IntegerField(help_text="1 - 5")
    description = models.TextField()
    
    # Replaced storage_key/content_type with ImageField for easier handling
    image = models.ImageField(upload_to='munro_images/', blank=True)
    
    # optional
    estimated_time_hours = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class ClimbRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    munro = models.ForeignKey(Munro, on_delete=models.CASCADE)
    climb_date = models.DateField()
    total_meters_climbed = models.IntegerField() # This might be redundant if it's just munro height, but maybe they climbed partial? Assuming full climb.
    total_distance = models.IntegerField(help_text="Kilometres")
    completion_time_minutes = models.IntegerField()
    star_rating = models.IntegerField(help_text="1 - 5")
    created_at = models.DateTimeField(auto_now_add=True)
    
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.munro} (Climb Date: {self.climb_date})"

class Photo(models.Model):
    record = models.ForeignKey(ClimbRecord, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='climb_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.record}"

class UserFavouriteMunro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    munro = models.ForeignKey(Munro, on_delete=models.CASCADE)
    set_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Favourite: {self.munro.name}"
