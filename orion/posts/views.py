from django import template
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.http import Http404

from posts.models import Post

class PostDetailView(DetailView):

    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_title'] = 'Просмотр поста'
        return context