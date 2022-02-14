from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.urls import reverse

from posts.models import Post
from users.models import User
from users.forms import UserForm


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile.html'
    slug_field = 'username'


class UserPostListView(ListView):
    model = User
    context_object_name = 'posts'
    template_name = 'users/user_profile_posts.html'


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name_suffix = '_update_form'
    permission_required = 'users.can_update'
    # ToDo: add url for to redirect to a login form
    # login_url = reverse()

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:user_detail_pk', kwargs={'pk': pk})

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        if self.request.user.pk != self.kwargs['pk'] and not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True

