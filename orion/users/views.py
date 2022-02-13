from django.shortcuts import render
from django.views.generic import DetailView

from users.models import User
from users.forms import UserForm


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_profile.html'
    slug_field = 'username'


def user_create(request):
    form = UserForm()
    if request.method == 'POST':
        data = request.POST
        pass1 = data['pass1']
        pass2 = data['pass2']
        if pass1 != pass2:
            raise ValueError('пароли не совпадают!')

        user_fields = {'username': data['username'],
                       'name': data['name'],
                       'bio': data['bio'],
                       'birth_year': data['birth_year'],
                       'avatar': data['avatar'],
                       }
        User.objects.create_user(email=data['email'], password=pass1, **user_fields)

    context = {'form': form}
    return render(request, 'cabinet/index.html', context)
