from gtts import gTTS
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from pytils.translit import slugify
from django.core.files.storage import FileSystemStorage

from hub.models import Hub
from likes.models import LikeDislike
from notifications.models import Notification
from posts.models import Post


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/index.html'

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset)
        # only author and staff can see inactive post (draft, on moderation, etc)
        if post.status != 'ACTIVE':
            user = self.request.user
            # ToDo: change access rules after user groups implementation
            if user.is_anonymous or not (user == post.user or user.is_staff):
                raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments_list'] = self.object.comments.filter(active=True, parent__isnull=True)
        context['likes_count'] = self.object.votes.sum_rating()
        try:
            context['current_user_like'] = LikeDislike.objects.get(user=self.request.user, content_type__model='post',
                                                                   object_id=self.object.id).vote
        except LikeDislike.DoesNotExist:
            pass
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
        if action == 'moderation':
            Notification.create_notification(
                content_type=ContentType.objects.get(model='likedislike'),
                object_id=self.object.id,
                user_id=self.request.user.id,
                target_user_id=None,
            )
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


def text_to_voice_view(request, slug):
    if request.method == 'POST':
        text = request.POST.get('text')
        text = text.replace(u'\xa0', ' ')
        language = 'ru'

        path = f'speech/{str(slug)}.mp3'
        file = gTTS(text=text, lang=language, slow=False)

        file.save('media/' + path)

        return HttpResponse(path)
    return HttpResponse()
