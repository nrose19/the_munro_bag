from django.urls import path
from munro_app import views

app_name = 'munro_app'

urlpatterns = [
    path('', views.index, name='index'),

]