from django.urls import path
from munro_app import views

app_name = 'munro_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_profile/', views.user_profile, name='user_profile'),
]