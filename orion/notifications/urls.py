from django.urls import path

from . import views


app_name = 'notifications'
urlpatterns = [
    path('header/', views.get_notifications, name='get_notifications'),
]
