from django.urls import path
from tags import views

app_name = 'tags'
urlpatterns = [
    path('command/', views.TagCommandView.as_view(), name='tag-command'),
    path('list/', views.TagListView.as_view(), name='tag-query'),
]
