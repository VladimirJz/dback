# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from app.models import CompanyOffices, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CompanyOffices)
