from django.shortcuts import render
from munro_app.models import Munro, ClimbRecord, Photo, UserFavouriteMunro

# Create your views here.

def index(request):
    #need further code in here
    #context_dict = []

    return render(request, 'munro/index.html')

def user_profile(request):
    # need to add in our relevant models 
    
    # context_dict = {}

    # try: 
    #     munro = Munro.objects.get()

    return render(request, 'munro/user_profile.html')