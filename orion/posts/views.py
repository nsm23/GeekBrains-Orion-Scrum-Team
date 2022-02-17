from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage

from posts.models import Post


class PostDetailView(DetailView):

    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_hub'] = self.object.hub.alias
        context['page_title'] = 'Хаб | ' + self.object.hub.title + ' | Просмотр поста — ' + self.object.title
        context['comments_list'] = self.object.comments.filter(active=True, parent__isnull=True)

        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'brief_text', 'text', 'image', 'hub']

    def form_valid(self, form):
        self.object = form.save()
        publish = 'publish' in self.request.POST
        self.object.status = Post.ArticleStatus.ACTIVE if publish else Post.ArticleStatus.DRAFT
        self.object.slug = slugify(self.object.title)
        self.object.user = self.request.user
        post_image = self.request.FILES['image']
        fs = FileSystemStorage()
        fs.save(post_image.name, post_image)

        self.object.save()
        if publish:
            return HttpResponseRedirect(reverse('main'))
        return HttpResponseRedirect(reverse('cabinet:user_profile',
                                            kwargs={'pk': self.request.user.id, 'section': 'user_drafts'}))