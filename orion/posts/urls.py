from django.urls import path
from posts import views


app_name = 'posts'
urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='create-post'),
    path('edit/<slug:slug>', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>', views.PostDeleteView.as_view(), name='delete'),
    path('speech/<slug:slug>', views.text_to_voice_view, name='speech'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='detail'),
    path('tag/<slug:slug>', views.ListTagView.as_view(), name='tag'),
]
