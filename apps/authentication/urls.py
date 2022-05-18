# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

from ..home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile.html", views.loan, name="loan"),
    path("investor_profile.html", views.investments, name="investments"),
    path("investor.html", views.investor_page, name="investor_page"),
    path('investor_profile.html', views.invest, name="invest"),
    path('profile/', views.profile, name="profile")
]
