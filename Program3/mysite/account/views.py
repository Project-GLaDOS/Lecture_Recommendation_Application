import re

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import auth

from .models import UserAccount


def index(request):
    return render(request, 'account/sign_in.html', {})


def sign_in(request):
    email = request.POST['user_email']
    pw = request.POST['user_pw']

    if email == '':
        return render_sign_in(request, 'error_email', '메일을 입력해주세요')

    if not re.search("[0-9a-zA-Z]+[@][a-zA-Z]+[.][a-zA-Z]+", email):
        return render_sign_in(request, 'error_email', '메일 형식이 잘못되었습니다')

    if pw == '':
        return render_sign_in(request, 'error_pw', '비밀번호를 입력해주세요')

    user = auth.authenticate(request, username=email, password=pw)
    if user is not None:
        auth.login(request, user)
        return HttpResponse("sign in succeed!!<br>id: %s" % request.POST['user_email'])
    else:
        return render_sign_in(request, 'error_email', '메일 또는 비밀번호가 틀렸습니다')


def find_email(request):
    return HttpResponse("Find email")


def find_password(request):
    return HttpResponse("Find password")


def show_sign_up(request):
    return render(request, 'account/sign_up.html', {})


def sign_up(request):
    email = request.POST['user_email']
    pw = request.POST['user_pw']
    pw_confirm = request.POST['user_pw_confirm']

    if email == '':
        return render_sign_up(request, 'error_email', '메일을 입력해주세요')

    if not re.search("[0-9a-zA-Z]+[@][a-zA-Z]+[.][a-zA-Z]+", email):
        return render_sign_up(request, 'error_email', '메일 형식이 잘못되었습니다')

    if pw == '':
        return render_sign_up(request, 'error_pw', '비밀번호를 입력해주세요')

    if not re.search(".{7}", pw):
        return render_sign_up(request, 'error_pw', '비밀번호를 7자 이상 입력해주세요')

    if pw_confirm == '':
        return render_sign_up(request, 'error_pw_confirm', '비밀번호를 한 번 더 입력해주세요')

    if pw != pw_confirm:
        return render_sign_up(request, 'error_pw_confirm', '비밀번호가 일치하지 않습니다')

    try:
        User.objects.create_user(email, None, pw)
        return HttpResponse("sign up succeed!!<br>id: %s" % request.POST['user_email'])
    except IntegrityError:
        return render_sign_up(request, 'error_email', '이미 가입된 메일입니다')


def render_sign_in(request, err_name, err_str):
    email = request.POST['user_email']
    pw = request.POST['user_pw']

    return render(request, 'account/sign_in.html',
                  {
                      'user_email': email,
                      'user_pw': pw,
                      err_name: err_str
                  })


def render_sign_up(request, err_name, err_str):
    email = request.POST['user_email']
    pw = request.POST['user_pw']
    pw_confirm = request.POST['user_pw_confirm']

    return render(request, 'account/sign_up.html',
                  {
                      'user_email': email,
                      'user_pw': pw,
                      'user_pw_confirm': pw_confirm,
                      err_name: err_str
                  })
