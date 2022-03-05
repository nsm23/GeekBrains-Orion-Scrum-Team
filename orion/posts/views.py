from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from pytils.translit import slugify
from django.core.files.storage import FileSystemStorage

from hub.models import Hub
from posts.models import Post


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_list'] = self.object.comments.filter(active=True, parent__isnull=True)
        context['likes_count'] = self.object.votes.sum_rating()
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'brief_text', 'text', 'image', 'hub']

    def form_valid(self, form):
        self.object = form.save()
        publish = 'publish' in self.request.POST
        if publish and self.request.user.rating >= Post.MIN_USER_RATING_TO_PUBLISH:
            action = 'publish'
            self.object.status = Post.ArticleStatus.ACTIVE
            redirect_name, section = 'main', None
        elif publish:
            action = 'moderation'
            self.object.status = Post.ArticleStatus.MODERATION
            redirect_name, section = 'cabinet:user_profile', 'user_moderation_posts'
        else:
            action = 'draft'
            self.object.status = Post.ArticleStatus.DRAFT
            redirect_name, section = 'cabinet:user_profile', 'user_drafts'
        self.object.slug = slugify(self.object.title + str(self.object.id))
        self.object.user = self.request.user
        if 'image' in self.request:
            post_image = self.request.FILES['image']
            fs = FileSystemStorage()
            fs.save(post_image.name, post_image)

        self.object.save()
        if action == 'publish':
            return HttpResponseRedirect(reverse('main'))
        return HttpResponseRedirect(reverse(redirect_name, kwargs={'pk': self.request.user.id, 'section': section}))


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'brief_text', 'text', 'image', 'hub', 'status']

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user.pk != post.user.pk and not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.title = request.POST['title']
        hub_id = request.POST['hub']
        self.object.hub = Hub.objects.get(id=hub_id)
        self.object.brief_text = request.POST['brief_text']
        self.object.text = request.POST['text']
        publish = 'publish' in request.POST
        self.object.status = Post.ArticleStatus.ACTIVE if publish else Post.ArticleStatus.DRAFT
        self.object.slug = slugify(self.object.title + str(self.object.id))
        if 'image' in request:
            post_image = request.FILES['image']
            fs = FileSystemStorage()
            fs.save(post_image.name, post_image)

        self.object.save()
        if publish:
            return HttpResponseRedirect(reverse('main'))
        return HttpResponseRedirect(reverse('cabinet:user_profile',
                                            kwargs={'pk': self.request.user.id, 'section': 'user_drafts'}))


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('main')
    template_name = 'posts/post_delete.html'

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        if self.request.user.pk != post.user.pk and not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True
