from django.urls import path

from . import views


app_name = 'notifications'
urlpatterns = [
    path('user/<str:content_type>/', views.get_notifications, name='get_notifications'),
]
