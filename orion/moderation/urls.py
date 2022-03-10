from django.urls import path

from . import views


app_name = 'moderation'
urlpatterns = [
    path('posts/', views.PostModerationListView.as_view(), name='posts_on_moderation'),
    path('posts/approve/<int:post_id>/', views.approve_post_publishing, name='post_approve'),
    path('posts/decline/<int:post_id>/', views.decline_post_publishing, name='post_decline'),
]
