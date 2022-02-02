from pkgutil import iter_modules
from statistics import mode
from django.db import models
#from sqlalchemy import null
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    LocationName=models.CharField(max_length=30,verbose_name='Location',help_text='Location name')
    pass


class ItemCategory(models.Model):
    CategoryName=models.CharField(max_length=30,verbose_name='Category',help_text='Category')

class ItemStatus(models.Model):
    Status=models.CharField(max_length=10,help_text='Item Status',verbose_name='Item status')

class Item(models.Model):
    Description=models.CharField(max_length=100,)
    Category=models.ForeignKey(ItemCategory,on_delete=models.SET_NULL,null=True,blank=True)
    Status=models.ForeignKey(ItemStatus,on_delete=models.SET_NULL,null=True,blank=True)
    InternalID=models.CharField(max_length=100,help_text='Internal Id',blank=True)
    Brand=models.CharField(max_length=30,help_text='Item Brand',blank=True)
    Model=models.CharField(max_length=30,help_text='Item Model',blank=True)
    SerialNumber=models.CharField(max_length=100,help_text='SN',blank=True)
    SKU=models.CharField(max_length=100,help_text='SKU',blank=True)
    Color=models.CharField(max_length=30,help_text='Item color',blank=True)
    Dimensions=models.CharField(max_length=30,help_text='Item Size',blank=True)
    AssignedTo=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

class IssuesType(models.Model):
    Description=models.CharField(max_length=30)

class Issues(models.Model):
    Type=models.ForeignKey(IssuesType,on_delete=models.SET_NULL,null=True)
    Description=models.CharField(max_length=20,help_text='Issue Description')
    Date=models.DateField(help_text='Issue Date')