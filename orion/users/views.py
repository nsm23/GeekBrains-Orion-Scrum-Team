from django.shortcuts import render
from users.models import User
from users.forms import UserForm


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


def user_detail(request, user_id=0):
    form = UserForm()
    if request.method == 'GET':
        user = User.objects.get(pk=user_id)
        form = UserForm(instance=user)

    context = {'form': form}
    return render(request, 'cabinet/index.html', context)
