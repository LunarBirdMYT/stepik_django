from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError



def signupuser(request):
    if request.method == 'POST':
        if request.POST['password1'] != request.POST['password2']:
            return render(
                    request,
                    'todo/singupuser.html',
                    {'form': UserCreationForm(),
                    'error': 'Пароль не корректен'}
                    )
        try:
            user = User.objects.create_user(
                request.POST['username'],
                password=request.POST['password1']
                )
            user.save()
            login(request, user)
            return redirect('currenttodos')
        except IntegrityError:
            return render(
                request,
                'todo/singupuser.html',
                {'form': UserCreationForm(),
                'error': 'Имя пользователя уже используется. Задайте новое.'}
                )
    return render(request, 'todo/singupuser.html', {'form': UserCreationForm()})


def currenttodos(request):
     return render(request, 'todo/currenttodos.html')
