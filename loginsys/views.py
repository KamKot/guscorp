# coding=utf-8
from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from pererabotka.models import brigada
from pererabotka import models


# Create your views here.
def login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/pererabotka/')
        else:
            args['login_error'] = 'Неверное имя пользователя или пароль'
            return render_to_response('loginsys.html', args)
    else:
        return render_to_response("loginsys.html", args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.method == 'POST':
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            a = models.brigada(name=newuser)
            a.save()
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
