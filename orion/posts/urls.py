from django.urls import path
from .views import PostDetailView
from django.conf import settings


app_name = 'posts'
urlpatterns = [
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
