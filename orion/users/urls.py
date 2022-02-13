from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('', views.user_create, name='user_create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail_pk'),
    path('<str:slug>/', views.UserDetailView.as_view(), name='user_detail_slug'),
]
