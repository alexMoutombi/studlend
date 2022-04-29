# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    PROFILE_PERSON = (
        ('INVESTOR', 'Investor'),
        ('STUDENT', 'Student'),
    )
    profile = models.CharField(max_length=10, choices=PROFILE_PERSON)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s the person" % self.name

class Student(Person):
    desire_amount = models.IntegerField()
    loan_period = models.IntegerField()
    cumulative_income = models.IntegerField()
    school = models.CharField(max_length=100, null=True)
    school_rank = models.IntegerField()
    score_loan = models.IntegerField(default=10)

    def __str__(self):
        return "%s the student" % self.name

class Investor(Person):
    pass
    amount_invest = models.IntegerField()
    investment_duration = models.IntegerField()
    geolocation = models.CharField(max_length=100)

    def __str__(self):
        return "%s the investor" % self.name

class UserProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    investor = models.OneToOneField(Investor, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.student.name

    def __str__(self):
        return self.investor.name

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])


class Investment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    amount_invest = models.IntegerField()
    investment_date = models.DateField()
    investment_duration = models.IntegerField()

    def __str__(self):
        return "%s the investment" % self.name

class Loan(models.Model):
    person = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()
    borrowing_date = models.DateField(auto_now=True)
    repayment_date = models.DateField(null=True)
    loan_duration = models.IntegerField()
    LOAN_STATE = (
        ('P', 'Pending'),
        ('D', 'Done'),
    )
    loan_state = models.CharField(max_length=1, choices=LOAN_STATE, default='P')
    rate = models.IntegerField()

    def __str__(self):
        return "%s the loan" % self.name


