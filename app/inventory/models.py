from pkgutil import iter_modules
from django.db import models
#from sqlalchemy import null
from django.contrib.auth.models import User
from app.company.models import Employ

# Create your models here.

class Location(models.Model):
    LocationName=models.CharField(max_length=30,verbose_name='Location',help_text='Location name')
    pass


class ItemCategory(models.Model):
    CategoryName=models.CharField(max_length=30,verbose_name='Category',help_text='Category')

    # Accesorio de computo
    # Equipo de Computo
    # Equipo de Comunicaciones
    # Herramienta y Equipo
    # Mobiliario
    # Software 6
    

class ItemStatus(models.Model):
    StatusName=models.CharField(max_length=10,help_text='Item Status',verbose_name='Item status')

    def __str__(self):
        return self.Status
    #Activo 1
    #Baja

class ItemCondition(models.Model):
    ConditionName=models.CharField(max_length=30,help_text='Item Condition',verbose_name='Item condition')
    def __str__(self):
        return self.Condition
# Nuevo 1
# Usado
# Reparado
# Dañado

class Item(models.Model):
    Description=models.CharField(max_length=200)
    Category=models.ForeignKey(ItemCategory,on_delete=models.SET_NULL,null=True,blank=True)
    Status=models.ForeignKey(ItemStatus,on_delete=models.SET_NULL,null=True,blank=True)
    InternalID=models.CharField(max_length=100,help_text='Internal Id',null=True,blank=True)
    Brand=models.CharField(max_length=30,help_text='Item Brand',null=True,blank=True)
    Model=models.CharField(max_length=30,help_text='Item Model',null=True,blank=True)
    SerialNumber=models.CharField(max_length=100,help_text='SN',null=True,blank=True)
    SKU=models.CharField(max_length=100,help_text='SKU',null=True,blank=True)
    Color=models.CharField(max_length=30,help_text='Item color',null=True,blank=True)
    Dimensions=models.CharField(max_length=30,help_text='Item Size',null=True,blank=True)
    Employ=models.ForeignKey(Employ,on_delete=models.SET_NULL,null=True)
    Condition=models.ForeignKey(ItemCondition,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.Description[:80]

    

        

class IssuesType(models.Model):
    Description=models.CharField(max_length=30)
    def __str__(self):
        return self.Description[:80]

class Issues(models.Model):
    Type=models.ForeignKey(IssuesType,on_delete=models.SET_NULL,null=True)
    Description=models.CharField(max_length=20,help_text='Issue Description')
    Date=models.DateField(help_text='Issue Date')