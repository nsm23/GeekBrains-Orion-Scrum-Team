from django.views.generic.detail import DetailView
from posts.models import Post


class PostDetailView(DetailView):

    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'Хаб | ' + self.object.hub.title + ' | Просмотр поста — ' + self.object.title
        return context
