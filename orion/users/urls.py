from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail_pk'),
    path('<str:slug>/', views.UserDetailView.as_view(), name='user_detail_slug'),
]
