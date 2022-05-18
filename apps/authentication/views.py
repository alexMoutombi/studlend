# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from ..home.models import Person


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # email = form.cleaned_data.get("email")
            person = authenticate(username=username, password=password)
            # print(Person.objects.all())
            if person is not None:
                if username in ['alexmyar', 'Armand', 'Cedric', 'Dave', 'Cosmos', 'Giovani']:
                    login(request, person)
                    print(person)
                    return redirect("/investor.html")
                elif username in ["Allan", 'Kevin', 'Loic', 'Gaetan', 'Joel']:
                    login(request, person)
                    print(person)
                    return redirect("/loan.html")
                else:
                    login(request, person)
                    print(person)
                    return redirect("/admin_profile.html")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            profile = form.cleaned_data.get("profile")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, email=email, profile=profile, password=raw_password)
            print(profile)

            msg = 'User created - please login.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
