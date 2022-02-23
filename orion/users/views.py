from django.contrib import auth
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from django.urls import reverse, reverse_lazy

from posts.models import Post
from users.models import User
from users.forms import UserForm, RegisterForm, LoginForm


def login(request):
    if request.method == 'POST':
        form_login = LoginForm(data=request.POST)

        print(form_login)
        if form_login.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                # return HttpResponse('Authenticated successfully')
                return HttpResponseRedirect(reverse_lazy('main'))
            else:
                return HttpResponse('Disabled account')
    else:
        form_login = LoginForm()

    context = {
        'form_login': form_login,
    }
    return render(request, 'users/user_login.html', context)


def register(request):
    if request.method == 'POST':
        form_reg = RegisterForm(request.POST)
        if form_reg.is_valid():
            user = form_reg.save(commit=False)
            user.set_password(form_reg.cleaned_data['password'])
            user.save()
            return render(request, 'users/user_reg_done.html', {'user': user})
    else:
        form_reg = RegisterForm()
    return render(request, 'users/user_register.html', {'form_reg': form_reg})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('main'))


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
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('users:user_profile', kwargs={'pk': pk, 'section': 'user_detail'})

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        if self.request.user.pk != self.kwargs['pk'] and not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True
