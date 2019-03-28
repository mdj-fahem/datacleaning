from django.contrib import admin
from django.urls import path
from . import views

app_name = "datacleaning"

urlpatterns = [
    path('', views.home, name="homepage"),
    path('register', views.register, name="register"),
    path('logout', views.logout_request, name="logout"),
    path('login', views.login_request, name="login"),
    path('result', views.adress, name="adress"),
    path('account', views.account, name="account"),
    path('search', views.search, name="search"),
    path('delete', views.delete_account, name="delete"),

]