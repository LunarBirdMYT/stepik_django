from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError

from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')

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


def loginuser(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
            'error': 'Пароль не верный или пользователя не существует.'})
        login(request, user)
        return redirect('currenttodos')
    return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def createtodo(request):
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/createtodo.html',
                {'form': TodoForm(), 'error': 'Ошибка в веденных данных!'})

    return render(request, 'todo/createtodo.html', {'form': TodoForm()})


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})
