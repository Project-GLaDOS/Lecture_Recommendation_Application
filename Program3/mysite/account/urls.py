from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in_pressed/', views.sign_in, name='sign_in'),
    path('find_email/', views.find_email, name='find_email'),
    path('find_password/', views.find_password, name='find_password'),
    path('sign_up/', views.show_sign_up, name='show_sign_up'),
    path('sign_up_pressed/', views.sign_up, name='sign_up'),
]