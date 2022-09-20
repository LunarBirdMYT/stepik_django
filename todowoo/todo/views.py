from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone

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

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
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

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=False).order_by('-datecomplited')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(
                request,
                'todo/viewtodo.html',
                {'todo': todo, 'form': form, 'error': 'Неверная информация!'})
    form = TodoForm(instance=todo)
    return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecomplited = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')