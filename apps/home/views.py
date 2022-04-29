# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
import math

from django.utils.datetime_safe import datetime

from apps.home.models import Loan, Student, Investor, UserProfile


# @login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def profile(request):
    context = {
    }

    html_template = loader.get_template('/profile.html')
    return render('/profile.html', request, context)

# @login_required(login_url="/login/")
def pages(request):
    context = {

    }
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def taux_loan(age: int, school_rank: int, incoming_parent: int, loan_duration: int, mber_familly_worker: int,
              nber_internship: int, nber_jobs: int):
    taux = 1000
    # taux age
    if age > 27 or age < 18:
        taux += 0
    else:
        taux += ((27 - age) * -10)

    # taux de revenu
    if incoming_parent >= 80000:
        taux += 50
    elif incoming_parent < 20000:
        taux += 0
    else:
        taux += ((math.ceil((incoming_parent - 20000) / 10000)) * -10)

    # taux ecole
    taux += math.floor(school_rank / 10) * 10

    # duree pret
    if loan_duration in [1, 2, 3]:
        taux += (loan_duration * -10)

    # membres de la famille directe qui travaillent
    taux += mber_familly_worker * -10

    # stages effectués et jobs
    taux += (nber_jobs + nber_internship) * -10

    return taux / 100


def loan(request):
    global age, school_rank, incoming_parent, loan_duration, mber_familly_worker, nber_internship, nber_jobs
    print(request.method == 'POST')
    if request.method == 'POST':
        name = request.user.get_username
        surname = request.user.get_username
        amount = request.POST['amount']
        age = request.POST['age']
        school_rank = request.POST['school_rank']
        incoming_parent = request.POST['incoming_parent']
        loan_duration = request.POST['loan_duration']
        mber_familly_worker = request.POST['mber_familly_worker']
        nber_internship = request.POST['nber_internship']
        nber_jobs = request.POST['nber_jobs']
        borrowing_date = datetime.now()

    rate = taux_loan(int(age), int(school_rank), int(incoming_parent), int(loan_duration), int(mber_familly_worker), int(nber_internship), int(nber_jobs))
    student = Student.objects.create(name=name, surname = surname, age = int(age), desire_amount = int(amount), loan_period = int(loan_duration), cumulative_income = int(incoming_parent),
                                     school_rank = int(school_rank), score_loan = rate)
    student.save()

    loan = Loan.objects.create(person = student, loan_duration=loan_duration, amount=amount,
                               rate=rate)
    loan.save()
    total_amount = rate*float(amount) + float(amount)
    # messages.success(request, 'Data has been submited')
    return render(request, 'home/profile.html', context= {'rate': rate, 'amount': amount, 'loan_duration':loan_duration, 'total_amount': total_amount})
