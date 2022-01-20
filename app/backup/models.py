from typing import Tuple
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, SmallIntegerField
from django.db.models.fields.related import ForeignKey
from app.catalog.models import Tables,DataBases

# Create your models here.



class Jobs(models.Model):
    JobName=models.CharField(max_length=50,help_text='Backup Job name');
    def __str__(self):
        return self.JobName

class Locations(models.Model):
    LocationName=models.CharField(max_length=50,help_text='Location name');
    FilesPath=models.CharField(max_length=200,help_text='Location path')  ;  
     
    def __str__(self):
        return self.LocationName


class Status(models.Model):
    Status=models.CharField(max_length=20,help_text='Status');
    Description=models.CharField(max_length=200,help_text='Status description')
    
    def __str__(self):
        return self.Status

class Backups(models.Model):
    Database=models.ForeignKey(DataBases,on_delete=models.SET_NULL,null=True);
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    Status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True);
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True);
    CreationDate=models.DateField(null=True,blank=True,help_text='Create date');
    StartBackup=models.DateTimeField(null=True,blank=True,help_text='Backup start time');
    EndBackup=models.DateTimeField(null=True,blank=True,help_text='Backup end time');
    FileName=models.CharField(max_length=100,help_text='File name');
    SizeMB=models.DecimalField(max_digits=20,decimal_places=2,help_text='Size MB');
    Size=models.BigIntegerField(help_text='Size');
    Comments=models.TextField(help_text='Comments')
    class Meta:
     db_table = "backup_files"

    def __str__(self):
            return self.FileName

class Rotation(models.Model):
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    Order=SmallIntegerField(help_text='No.Rule');
    Rule=CharField(help_text="Rule rotation name",max_length=40,null=False);
    RULE_STATUS = [(1, 'Enable'),(2, 'Disable'),];
    Status= models.SmallIntegerField(choices=RULE_STATUS,default=1);
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True);
    RetentionDays=SmallIntegerField(help_text='Retention days',null=False);
    FileFormat=CharField(max_length=6,help_text='Backup format', null=False);
    def __str__(self):
        return 'On ' + self.Rule + ' for ' + self.RetentionDays 

