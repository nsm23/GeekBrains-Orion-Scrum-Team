from django.views.generic import ListView, CreateView
from tags.models import Tag


class TagCommandView(CreateView):
    model = Tag
    fields = '__all__'


class TagListView(ListView):
    model = Tag
