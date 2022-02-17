from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('<int:pk>', views.UserProfileView.as_view(), name='user_detail'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<int:pk>/<str:section>/', views.UserProfileView.as_view(), name='user_profile'),
]
