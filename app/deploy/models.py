from typing import TextIO
from django.core.checks.messages import DEBUG
from django.db import models

# Create your models here.
from datetime import date
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField, SmallIntegerField, TextField
from django.db.models.fields.related import ForeignKey
from app.catalog.models import DataBases, Tables



class Jobs(models.Model):
    Job=CharField(max_length=50,help_text='Job Name')
    SourceDB=ForeignKey(DataBases,on_delete=models.SET_NULL,null=True, related_name='SourceOf')
    TargetDB=CharField(max_length=50,help_text='Destination Database')
    Created=DateField(default=date.today)
    
    def __str__(self):
        return self.Job


# class JobTables:
#     Job=ForeignKey(Jobs,on_delete=models.SET_NULL,null=True)
#     Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)    

class TableFilters(models.Model):
    Job=models.ManyToManyField(Jobs)
    Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)
    Column=CharField(max_length=50,help_text='Column Name')
    FILTERS_TYPES=[(0,'Dont Filter'),(1,'Equal to'),(2,'Between'),(3,'Iterate Between')];
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
    SCRIPT_TYPES =[(1,'DDL'),(2,'DML'),(3,'Other')]
    SCRIPT_PHASES=[(1,'Building Objects'),(2,'Transfer Data'),(3,'Relational Objects'),(4,'Ending database')]
    Job=ForeignKey(Jobs,on_delete=models.SET_NULL,null=True)
    Type=models.SmallIntegerField(choices=SCRIPT_TYPES,help_text='Type of script')
    Phase=models.SmallIntegerField(choices=SCRIPT_PHASES,help_text='Phase of execution',null=True,blank=True,default=1)
    Order=IntegerField(help_text='Order of exec')
    Script=TextField(help_text='Sentence SQL to execute',null=True)



