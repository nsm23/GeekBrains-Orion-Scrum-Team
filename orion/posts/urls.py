from django.urls import path
from .views import PostDetailView, PostCreateView


app_name = 'posts'
urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create-post'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
]
