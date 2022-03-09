from django.urls import path

from . import views


app_name = 'moderation'
urlpatterns = [
    path('posts/', views.PostModerationListView.as_view(), name='posts_on_moderation'),
]
