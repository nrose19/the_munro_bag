from django.shortcuts import render

# Create your views here.

def index(request):
    #need further code in here
    #context_dict = []

    return render(request, 'index.html')