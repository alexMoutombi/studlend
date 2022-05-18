# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import Person


# class PersonAdmin(UserAdmin):
#     list_display = (
#         'name', 'surname', 'age', 'email', 'ville', 'phone', 'profile'
#         'is_investor', 'is_student', 'is_admin', 'mailing_address'  #'first_name', 'last_name', 'is_staff'
#     )
#
#     fieldsets = (
#         (None, {
#             'fields': ('username', 'password')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#             )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#         ('Additional info', {
#             'fields': ('is_student', 'is_investor', 'mailing_address')
#         })
#     )
#
#     add_fieldsets = (
#         (None, {
#             'fields': ('username', 'password1', 'password2')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#             )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#         ('Additional info', {
#             'fields': ('is_student', 'is_investor', 'mailing_address')
#         })
#     )
#
#
# admin.site.register(Person, UserAdmin)
