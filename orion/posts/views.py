from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage

from hub.models import Hub
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
        if 'image' in self.request:
            post_image = self.request.FILES['image']
            fs = FileSystemStorage()
            fs.save(post_image.name, post_image)

        self.object.save()
        if publish:
            return HttpResponseRedirect(reverse('main'))
        return HttpResponseRedirect(reverse('cabinet:user_profile',
                                            kwargs={'pk': self.request.user.id, 'section': 'user_drafts'}))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'brief_text', 'text', 'image', 'hub', 'status']

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.title = request.POST['title']
        hub_id = request.POST['hub']
        self.object.hub = Hub.objects.get(id=hub_id)
        self.object.brief_text = request.POST['brief_text']
        self.object.text = request.POST['text']
        publish = 'publish' in request.POST
        self.object.status = Post.ArticleStatus.ACTIVE if publish else Post.ArticleStatus.DRAFT
        self.object.slug = slugify(self.object.title)
        if 'image' in request:
            post_image = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(post_image.name, post_image)

        self.object.save()
        if publish:
            return HttpResponseRedirect(reverse('main'))
        return HttpResponseRedirect(reverse('cabinet:user_profile',
                                            kwargs={'pk': self.request.user.id, 'section': 'user_drafts'}))


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('main')
    template_name = 'posts/post_delete.html'
