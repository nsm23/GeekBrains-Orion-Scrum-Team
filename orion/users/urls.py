from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail_pk'),
    path('<str:slug>/', views.UserDetailView.as_view(), name='user_detail_slug'),
]
