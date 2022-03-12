from django.urls import path
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, text_to_voice_view


app_name = 'posts'
urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create-post'),
    path('edit/<slug:slug>', PostUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='delete'),
    path('speech/<slug:slug>', text_to_voice_view, name='speech'),
    path('<slug:slug>', PostDetailView.as_view(), name='detail'),
]
