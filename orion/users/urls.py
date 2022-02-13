from django.urls import path
from .views import user_detail, user_create


app_name = 'users'
urlpatterns = [
    path('', user_create, name='user_create'),
    path('<int:user_id>', user_detail, name='user_detail'),
]
