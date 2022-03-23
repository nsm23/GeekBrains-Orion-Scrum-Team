<<<<<<< Updated upstream
from django.urls import path
from posts import views
=======
from django.urls import path, include
>>>>>>> Stashed changes

from .views import (PostDetailView, PostCreateView,
                    PostUpdateView, PostDeleteView,
                    text_to_voice_view)

app_name = 'posts'
urlpatterns = [
<<<<<<< Updated upstream
    path('create/', views.PostCreateView.as_view(), name='create-post'),
    path('edit/<slug:slug>', views.PostUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>', views.PostDeleteView.as_view(), name='delete'),
    path('speech/<slug:slug>', views.text_to_voice_view, name='speech'),
    path('<slug:slug>', views.PostDetailView.as_view(), name='detail'),
    path('tag/<slug:slug>', views.ListTagView.as_view(), name='tag'),
=======
    path('create/', PostCreateView.as_view(), name='create-post'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('edit/<slug:slug>', PostUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='delete'),
    path('speech/<slug:slug>', text_to_voice_view, name='speech'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),

>>>>>>> Stashed changes
]
