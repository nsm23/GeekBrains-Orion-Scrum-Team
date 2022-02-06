from django.views.generic import ListView

from posts.models import Post


class MainView(ListView):
    model = Post
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        queryset = Post.objects.all().order_by('-created_at')[:12]
        context = super().get_context_data(object_list=queryset, **kwargs)
        context['page_title'] = 'Главная'
        return context
