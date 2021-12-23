from django.db import models

# Create your models here.
from datetime import date
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField, SmallIntegerField
from django.db.models.fields.related import ForeignKey
from app.catalog.models import DataBases, Tables



class Jobs(models.Model):
    Job=CharField(max_length=50,help_text='Job Name')
    SourceDB=ForeignKey(DataBases,on_delete=models.SET_NULL,null=True)
    TargetDB=CharField(max_length=50,help_text='Destination Database')
    Created=DateField(default=date.today)
    



# class JobTables:
#     Job=ForeignKey(Jobs,on_delete=models.SET_NULL,null=True)
#     Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)    

class TableFilters(models.Model):
    Job=models.ManyToManyField(Jobs)
    Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)
    Column=CharField(max_length=50,help_text='Column Name')
    FILTERS_TYPES=[(0,'Dont Filter')(1,'Equal to'),(2,'Between'),(3,'Iterate Between')];
    FilterType=models.SmallIntegerField(choices=FILTERS_TYPES, default=1,help_text='Filter by')
    LowerValue=CharField(max_length=10,help_text='Lower limit')
    UpperValue=CharField(max_length=10,help_text='Upper limit')
    DATA_TYPES=[(1,'Numeric'),(2,'String'),(3,'Date')]
    ValuesDataType=models.SmallIntegerField(choices=DATA_TYPES,default=0,help_text='Data type')
    StepBy=SmallIntegerField(help_text='Iterate over')


# class JobFilters:
#     Job=ForeignKey(Jobs,on_delete=models.SET_NULL,null=True)
#     TableFilter=ForeignKey(TableFilters,on_delete=models.SET_NULL,null=True)

class JobScripts(models.Model):
    Job=ForeignKey(Jobs,on_delete=models.SET_NULL,null=True)
    SCRIPT_TYPES=[(1,'DDL'),(2,'DML'),(3,'Other')]
    Type=models.SmallIntegerField(choices=SCRIPT_TYPES,help_text='Type of script')
    Order=IntegerField(help_text='Order of exec')



