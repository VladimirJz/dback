# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField, SmallIntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import ugettext_lazy as _
# Create your models here.

class CompanyOffices(models.Model):
    OfficeName=models.CharField(max_length=30,verbose_name='Office',help_text='Office name')
    def __str__(self):
        return self.OfficeName


class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    RFC =  CharField(max_length=50,help_text='RFC',blank=True)
    CURP=  CharField(max_length=50,help_text='CURP',blank=True)
    Office=ForeignKey(CompanyOffices,on_delete=models.SET_NULL,blank=True,null=True)
    BirthDate = models.DateField(null=True, blank=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.UserProfile.save()
    def __str__(self):
        return self.User.first_name