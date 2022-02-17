from django.contrib import auth
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, CreateView
from django.urls import reverse, reverse_lazy

from users.models import User
from users.forms import UserForm, RegisterForm, LoginForm


def login(request):
    if request.method == 'POST':
        form_login = LoginForm(data=request.POST)
        if form_login.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponse('Authenticated successfully')
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile.html'
    slug_field = 'username'


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
