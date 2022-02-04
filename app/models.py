# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from pyexpat import model
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField, SmallIntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import ugettext_lazy as _
# Create your models here.
