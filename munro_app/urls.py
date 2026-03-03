from django.urls import path
from munro_app import views

app_name = 'munro_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('add_climb/', views.add_climb, name='add_climb'),
    path('munros/', views.munro_list, name='munro_list'),
    path('munros/<int:munro_id>/', views.munro_detail, name='munro_detail'),
]
