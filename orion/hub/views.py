from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Q

from posts.models import Post
from hub.models import Hub


class HubView(ListView):
    template_name = 'hub/index.html'
    paginate_by = 12

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        hub = get_object_or_404(Hub, alias=slug)
        self.extra_context = {
            'page_title': f'Хаб | {hub}',
            'current_hub': slug,
        }
        return Post.objects.filter(Q(hub__alias=slug) & Q(status=Post.ArticleStatus.ACTIVE))


class MainView(ListView):
    template_name = 'index.html'
    paginate_by = 12
    extra_context = {'page_title': 'Главная'}
    queryset = Post.objects.filter(status=Post.ArticleStatus.ACTIVE)
