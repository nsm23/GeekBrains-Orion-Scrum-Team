from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.urls import reverse

from posts.models import Post
from users.models import User
from users.forms import UserForm


class UserProfileView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        user = kwargs.get('object')
        section = self.kwargs.get('section')
        if not section:
            section = 'user_detail'

        if section == 'user_posts':
            kwargs['posts'] = user.posts.filter(status=Post.ArticleStatus.ACTIVE)
        elif section == 'user_drafts':
            kwargs['posts'] = user.posts.filter(status=Post.ArticleStatus.DRAFT)

        kwargs['section'] = section

        return super().get_context_data(**kwargs)


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name_suffix = '_update_form'
    permission_required = 'users.can_update'
    # ToDo: add url for to redirect to a login form
    # login_url = reverse()

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:user_profile', kwargs={'pk': pk})

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        if self.request.user.pk != self.kwargs['pk'] and not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True

