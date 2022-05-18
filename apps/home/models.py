# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    PROFILE_PERSON = (
        ('INVESTOR', 'Investor'),
        ('STUDENT', 'Student'),
        ('ADMIN', 'Administrateur'),
    )
    profile = models.CharField(max_length=10, choices=PROFILE_PERSON)

    # @receiver(post_save, sender=User)
    # def create_user_user(sender, instance, created, **kwargs):
    #     if created:
    #         Person.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_user(sender, instance, **kwargs):
    #     instance.first_name.save()

    def __str__(self):
        return f"{self.user},{self.profile},{self.email}"

    def full_name(self):
        return f"{self.user[0]} {self.user[1]}"


class Student(Person):
    pass
    # id = models.BigAutoField(primary_key=True)
    # objects = models.Manager()
    # loan = models.ForeignKey('home.Loan', verbose_name='student_loan', on_delete=models.CASCADE)
    desire_amount = models.IntegerField()
    loan_period = models.IntegerField()
    cumulative_income = models.IntegerField()
    school = models.CharField(max_length=100, null=True)
    school_rank = models.IntegerField()
    score_loan = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name},{self.email},{self.user},{self.profile}"

    # class Meta:  # you have to add abstract class
    #     abstract = True


class Investor(Person):
    pass
    # id = models.BigAutoField(primary_key=True)
    # investment = models.ForeignKey('Investor', related_name='investor_investment', verbose_name='investor',
    #                                on_delete=models.CASCADE)
    amount_invest = models.IntegerField()
    investment_duration = models.IntegerField()
    geolocation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class UserProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    investor = models.OneToOneField(Investor, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.student.name},{self.investor.name}"


class Loan(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()
    borrowing_date = models.DateField(auto_now=True)
    repayment_date = models.DateField(null=True)
    loan_duration = models.IntegerField()
    percentage_invest = models.IntegerField(null=True, default=0)
    LOAN_STATE = (
        ('P', 'Pending'),
        ('D', 'Done'),
    )
    loan_state = models.CharField(max_length=1, choices=LOAN_STATE, default='P')
    rate = models.IntegerField()

    def __str__(self):
        return f"{self.amount},{self.student},{self.borrowing_date},{self.percentage_invest},{self.rate},{self.loan_duration}"


class Investment(models.Model):
    id = models.BigAutoField(primary_key=True)
    investor = models.ManyToManyField(Investor)
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    amount_invest = models.IntegerField()
    investment_date = models.DateField(auto_now=True)
    investment_duration = models.IntegerField()
    rendement = models.IntegerField()
    montant_attendu = models.IntegerField()
    profit = models.IntegerField()

    def __str__(self):
        return f"{self.amount_invest},{self.loan}"
