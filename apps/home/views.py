# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
import math

from django.utils.datetime_safe import datetime
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from apps.home.models import Loan, Student, Investor, UserProfile, Investment


# @login_required(login_url="/login/")
def index(request):
    loan = loan_home_page()
    print(loan)
    context = {'segment': 'index', 'loan': loan}

    # request.session['student_loan'] = {'student_name': loan.student, 'student_rate': loan.rate,
    #                                    'student_duration': loan.loan_duration, 'student_amount': loan.amount}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def investments(request):
    invesments = investment_page()
    print(invesments)
    context = {'investments': invesments}

    html_template = loader.get_template('home/investor_profile.html')
    return HttpResponse(html_template.render(context, request))


def investor_page(request):
    # student_loan = request.session.get('student_loan', None)
    # print(student_loan)
    loan = loan_home_page()
    context = {'loan': loan}

    html_template = loader.get_template('home/investor.html')
    return HttpResponse(html_template.render(context, request))


def profile(request):
    loans = loan_profile_page()
    print(loans)
    context = {'loans': loans}

    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


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
    taux = 400
    # taux age
    if age > 27 or age < 18:
        taux += 0
    else:
        taux += ((age - 18) * 10)

    # taux de revenu
    if incoming_parent < 20000 or 50000 <= incoming_parent <= 60000 or incoming_parent > 80000:
        taux += 0
    elif 20000 <= incoming_parent <= 30000:
        taux += 30
    elif 30000 <= incoming_parent <= 40000:
        taux += 20
    elif 40000 <= incoming_parent <= 50000:
        taux += 10
    elif 60000 <= incoming_parent <= 70000:
        taux -= 10
    elif 70000 <= incoming_parent <= 80000:
        taux -= 20
    else:
        taux += 0
        # taux += ((math.ceil((incoming_parent - 20000) / 10000)) * -10)

    # taux ecole
    taux += school_rank / 100

    # duree pret
    if loan_duration in [1, 2, 3]:
        taux += (loan_duration * 10)

    # membres de la famille directe qui travaillent
    taux += mber_familly_worker * -10

    # stages effectués et jobs
    taux += (nber_jobs + nber_internship) * -10

    if (taux / 100) < 4:
        taux = 4
        return taux
    else:
        return taux / 100


def loan(request):
    global age, school_rank, incoming_parent, loan_duration, mber_familly_worker, nber_internship, nber_jobs, surname, name, amount
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

    rate = taux_loan(int(age), int(school_rank), int(incoming_parent), int(loan_duration), int(mber_familly_worker),
                     int(nber_internship), int(nber_jobs))

    # user = User.objects.create_user(username=name, surname=surname)
    student = Student.objects.create(name=name, surname=surname, age=int(age), desire_amount=int(amount),
                                     loan_period=int(loan_duration), cumulative_income=int(incoming_parent),
                                     school_rank=int(school_rank), score_loan=rate)
    print(student)
    student.save()

    loan = Loan.objects.create(student=student, loan_duration=loan_duration, amount=amount,
                               rate=rate)
    loan.save()
    total_amount = (rate / 100) * float(amount) + float(amount)
    # messages.success(request, 'Data has been submited')
    loans = loan_profile_page()
    return render(request, 'home/profile.html',
                  context={'name': name, 'rate': rate, 'amount': amount, 'loan_duration': loan_duration,
                           'total_amount': total_amount, 'loans': loans})


def invest(request, loan_id=None):
    global amount_student, name, surname, investment_duration, percentage, rate_student
    print(request.method == 'POST')
    if request.method == 'POST':
        # name = request.user.get_username
        # surname = request.user.get_username
        percentage = request.POST['percentage']
        amount_student = request.POST['student_amount']
        investment_duration = request.POST['student_duration']
        rate_student = request.POST['student_rate']
        invest_date = datetime.now()

    amount_invest = float(percentage / 100) * float(amount_student)
    rendement = rate_student
    montant_attendu = float(amount_invest) * float(pow(1 + rendement, int(investment_duration)))
    profit = montant_attendu - amount_invest
    investment = Investment.objects.create(amount_invest=int(amount_invest),
                                           investment_duration=int(investment_duration), rendement=int(rendement),
                                           montant_attendu=int(montant_attendu), profit=int(profit))

    print("Alex Ok")
    investment.save()
    print(investment)

    return render(request, 'home/investor_profile.html',
                  context={'amount_invest': amount_invest, 'investment_duration': investment_duration,
                           'rendement': rendement, 'montant_attendu': montant_attendu, 'profit': profit})

    # return redirect('home/investor_profile.html')


# def investor_page(request):
#     investments = Investment.objects.all()
#
#     return render(request, 'home/investor_profile.html', context={'investments': investments})


def loan_home_page():
    try:
        loans = Loan.objects.all()  # exclude(percentage_invest=100). .aggregate(Max('percentage_invest'))
        loan = loans[0] if len(loans) > 0 else None
    except ObjectDoesNotExist:
        loan = None

    return loan


def loan_profile_page():
    try:
        # loan = Loan.objects.latest('borrowing_date')[:3]
        loan = Loan.objects.all()
        print(loan)
    except ObjectDoesNotExist:
        loan = None

    return loan


def investment_page():
    try:
        investment = Investment.objects.all()[:3]
        print(investment)
    except ObjectDoesNotExist:  # Investment.DoesNotExist
        investment = None

    return investment


@api_view(['GET'])
def loan_list(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        loan_list = loan
        return Response(loan_list.data)
