import re
from enum import Enum

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib import auth


class PageAddress(Enum):
    SIGN_IN = 'account/sign_in.html'
    SIGN_UP = 'account/sign_up.html'


class ErrorName(Enum):
    EMAIL = 'error_email'
    PW = 'error_pw'
    PW_CONFIRM = 'error_pw_confirm'


class FormName(Enum):
    EMAIL = 'user_email'
    PW = 'user_pw'
    PW_CONFIRM = 'user_pw_confirm'


class ErrorMessage(Enum):
    EMAIL_EMPTY = '메일을 입력해주세요'
    EMAIL_INVALID = '메일 형식이 잘못되었습니다'
    EMAIL_EXIST = '이미 가입된 메일입니다'
    SIGN_IN_ERROR = '메일 또는 비밀번호가 틀렸습니다'
    PW_EMPTY = '비밀번호를 입력해주세요'
    PW_SHORT = '비밀번호를 7자 이상 입력해주세요'
    PW_CONFIRM_EMPTY = '비밀번호를 한 번 더 입력해주세요'
    PW_CONFIRM_WRONG = '비밀번호가 일치하지 않습니다'


def index(request):
    return render(request, PageAddress.SIGN_IN.value)


def sign_in(request):
    email = request.POST[FormName.EMAIL.value]
    pw = request.POST[FormName.PW.value]

    err_name, err_str = check_error(email, pw)

    if err_name is not None:
        return render_custom(request, err_name, err_str)

    user = auth.authenticate(request, username=email, password=pw)
    if user is not None:
        auth.login(request, user)
        return HttpResponse("sign in succeed!!<br>id: %s" % request.POST[FormName.EMAIL.value])
    else:
        return render_custom(request, ErrorName.EMAIL.value, ErrorMessage.SIGN_IN_ERROR.value)


def find_email(request):
    return HttpResponse("Find email")


def find_password(request):
    return HttpResponse("Find password")


def show_sign_up(request):
    return render(request, PageAddress.SIGN_UP.value)


def sign_up(request):
    email = request.POST[FormName.EMAIL.value]
    pw = request.POST[FormName.PW.value]
    pw_confirm = request.POST[FormName.PW_CONFIRM.value]

    err_name, err_str = check_error(email, pw, pw_confirm)

    if err_name is not None:
        return render_custom(request, err_name, err_str)

    try:
        User.objects.create_user(email, None, pw)
        return HttpResponse("sign up succeed!!<br>id: %s" % request.POST[FormName.EMAIL.value])
    except IntegrityError:
        return render_custom(request, ErrorName.EMAIL.value, ErrorMessage.EMAIL_EXIST.value)


def check_error(email, pw, pw_confirm=None):
    if email == '':
        return ErrorName.EMAIL.value, ErrorMessage.EMAIL_EMPTY.value
    if not re.search("[0-9a-zA-Z]+[@][a-zA-Z]+[.][a-zA-Z]+", email):
        return ErrorName.EMAIL.value, ErrorMessage.EMAIL_INVALID.value
    if pw == '':
        return ErrorName.PW.value, ErrorMessage.PW_EMPTY.value
    if pw_confirm is not None:
        if not re.search(".{7}", pw):
            return ErrorName.PW.value, ErrorMessage.PW_SHORT.value
        if pw_confirm == '':
            return ErrorName.PW_CONFIRM.value, ErrorMessage.PW_CONFIRM_EMPTY.value
        if pw != pw_confirm:
            return ErrorName.PW_CONFIRM.value, ErrorMessage.PW_CONFIRM_WRONG.value
        else:
            return None, None
    else:
        return None, None


def render_custom(request, err_name, err_str):
    email = request.POST[FormName.EMAIL.value]
    pw = request.POST[FormName.PW.value]

    try:
        pw_confirm = request.POST[FormName.PW_CONFIRM.value]

        return render(request, PageAddress.SIGN_UP.value,
                      {
                          FormName.EMAIL.value: email,
                          FormName.PW.value: pw,
                          FormName.PW_CONFIRM.value: pw_confirm,
                          err_name: err_str
                      })
    except MultiValueDictKeyError:
        return render(request, PageAddress.SIGN_IN.value,
                      {
                          FormName.EMAIL.value: email,
                          FormName.PW.value: pw,
                          err_name: err_str
                      })
