import re
from enum import Enum

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import auth

from .models import UserAccount


class ErrorName(Enum):
    email = 'error_email'
    pw = 'error_pw'
    pw_confirm = 'error_pw_confirm'


class FormName(Enum):
    email = 'user_email'
    pw = 'user_pw'
    pw_confirm = 'user_pw_confirm'


class ErrorMessage(Enum):
    email_empty = '메일을 입력해주세요'
    email_invalid = '메일 형식이 잘못되었습니다'
    email_exist = '이미 가입된 메일입니다'
    sign_in_error = '메일 또는 비밀번호가 틀렸습니다'
    pw_empty = '비밀번호를 입력해주세요'
    pw_short = '비밀번호를 7자 이상 입력해주세요'
    pw_confirm_empty = '비밀번호를 한 번 더 입력해주세요'
    pw_confirm_wrong = '비밀번호가 일치하지 않습니다'


def index(request):
    return render(request, 'account/sign_in.html', {})


def sign_in(request):
    email = request.POST[FormName.email.value]
    pw = request.POST[FormName.pw.value]

    err_name, err_str = check_error(email, pw)

    if err_name is not None:
        return render_custom(request, err_name, err_str)

    user = auth.authenticate(request, username=email, password=pw)
    if user is not None:
        auth.login(request, user)
        return HttpResponse("sign in succeed!!<br>id: %s" % request.POST[FormName.email.value])
    else:
        return render_custom(request, ErrorName.email.value, ErrorMessage.sign_in_error.value)
        # check HttpRedirect


def find_email(request):
    return HttpResponse("Find email")


def find_password(request):
    return HttpResponse("Find password")


def show_sign_up(request):
    return render(request, 'account/sign_up.html', {})


def sign_up(request):
    email = request.POST[FormName.email.value]
    pw = request.POST[FormName.pw.value]
    pw_confirm = request.POST[FormName.pw_confirm.value]

    err_name, err_str = check_error(email, pw, pw_confirm)

    if err_name is not None:
        return render_custom(request, err_name, err_str)

    try:
        User.objects.create_user(email, None, pw)
        return HttpResponse("sign up succeed!!<br>id: %s" % request.POST[FormName.email.value])
    except IntegrityError:
        return render_custom(request, ErrorName.email.value, ErrorMessage.email_exist.value)


def check_error(email, pw, pw_confirm=None):
    if email == '':
        return ErrorName.email.value, ErrorMessage.email_empty.value
    if not re.search("[0-9a-zA-Z]+[@][a-zA-Z]+[.][a-zA-Z]+", email):
        return ErrorName.email.value, ErrorMessage.email_invalid.value
    if pw == '':
        return ErrorName.pw.value, ErrorMessage.pw_empty.value
    if pw_confirm is not None:
        if not re.search(".{7}", pw):
            return ErrorName.pw.value, ErrorMessage.pw_short.value
        if pw_confirm == '':
            return ErrorName.pw_confirm.value, ErrorMessage.pw_confirm_empty.value
        if pw != pw_confirm:
            return ErrorName.pw_confirm.value, ErrorMessage.pw_confirm_wrong.value
        else:
            return None, None
    else:
        return None, None


def render_custom(request, err_name, err_str):
    email = request.POST[FormName.email.value]
    pw = request.POST[FormName.pw.value]
    try:
        pw_confirm = request.POST[FormName.pw_confirm.value]

        return render(request, 'account/sign_up.html',
                      {
                          FormName.email.value: email,
                          FormName.pw.value: pw,
                          FormName.pw_confirm.value: pw_confirm,
                          err_name: err_str
                      })
    except MultiValueDictKeyError:
        return render(request, 'account/sign_in.html',
                      {
                          FormName.email.value: email,
                          FormName.pw.value: pw,
                          err_name: err_str
                      })
