from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Q

from posts.models import Post
from hub.models import Hub


class HubView(ListView):
    model = Post
    template_name = 'hub/index.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs["slug"] or ''
        queryset = Post.objects.filter(Q(hub__alias=slug) & Q(status=Post.ArticleStatus.ACTIVE)).order_by('-created_at')
        context = super().get_context_data(object_list=queryset, **kwargs)
        hub = get_object_or_404(Hub, alias=slug)
        context['page_title'] = f'Хаб | {hub.title}'
        context['current_hub'] = slug
        return context
