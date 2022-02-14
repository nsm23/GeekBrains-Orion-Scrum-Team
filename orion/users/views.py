from django.views.generic import DetailView, UpdateView
from django.urls import reverse

from users.models import User
from users.forms import UserForm


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile.html'
    slug_field = 'username'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:user_detail_pk', kwargs={'pk': pk})
