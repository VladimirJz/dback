from typing import Tuple
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, SmallIntegerField
from django.db.models.fields.related import ForeignKey
from app.catalog.models import Tables,DataBases

# Create your models here.






class Schedule(models.Model):
    pass

class RotationJob(models.Model):
    JobName=models.CharField(max_length=50,help_text='Rotation Job name');
    


class Locations(models.Model):
    LocationName=models.CharField(max_length=50,help_text='Location name');
    Host=models.CharField(max_length=30,help_text='Name or IP of host', null=True)
    AbsolutePath=models.CharField(max_length=200,help_text='Absolute(local) path to backup file',null=True)  ; 
    RemotePath=models.CharField(max_length=200,help_text='Destination Remote path',null=True,blank=True)  ;

     
    def __str__(self):
        return self.LocationName + ' (' + self.Host +')'
    class Meta:
        table_name='backup_locations'
        verbose_name_plural = "Locations"


class Jobs(models.Model):
    JobName=models.CharField(max_length=50,help_text='Backup Job name');
    Database=models.ForeignKey(DataBases,on_delete=models.SET_NULL,null=True,blank=True)
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True,blank=True)
    IsLocal=models.BooleanField(default=False, help_text='Is a local drive backup? ',verbose_name='Local backup')
    UseByPassDir=models.BooleanField(default=False, help_text='Use a bypass Dir? ',verbose_name='Use temporaly Dir')
    ByPassDir=models.CharField(max_length=200, help_text='Generate backup and move it later to Destination Dir',verbose_name='Temporaly Dir',blank=True,null=True)

    def __str__(self):
        return self.JobName
    class Meta:
        table_name='backup_jobs'
        verbose_name_plural = "Jobs"

class Status(models.Model):
    Status=models.CharField(max_length=20,help_text='Status');
    Description=models.CharField(max_length=200,help_text='Status description',null=True,blank=True)
    
    def __str__(self):
        return self.Description
    class Meta:
        table_name='backup_status'
        verbose_name_plural = "Status"

class Backups(models.Model):
    Database=models.ForeignKey(DataBases,on_delete=models.SET_NULL,null=True);
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    Status=models.ForeignKey(Status,on_delete=models.SET_NULL,null=True);
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True);
    CreationDate=models.DateField(null=True,blank=True,help_text='Create date');
    StartBackup=models.DateTimeField(null=True,blank=True,help_text='Backup start time');
    EndBackup=models.DateTimeField(blank=True,help_text='Backup end time',null=True);
    FileName=models.CharField(max_length=100,help_text='File name');
    SizeMB=models.DecimalField(max_digits=20,decimal_places=2,help_text='Size MB',null=True,default=0);
    Size=models.BigIntegerField(help_text='Size',null=True,default=0);
    Comments=models.TextField(help_text='Comments',null=True,blank=True)
    class Meta:
        db_table = "backup_files"
        verbose_name_plural = "Backups"

    def __str__(self):
            return self.FileName
  

class RotationRules(models.Model):
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    Order=SmallIntegerField(help_text='No.Rule');
    RuleName=CharField(help_text="Rule rotation name",max_length=40,null=False);
    RULE_STATUS = [(1, 'Enable'),(2, 'Disable'),];
    COMPRESS_FORMAT = [(1, '.zip'),(2, '.7z'),(3,'.tar')];
    Status= models.SmallIntegerField(choices=RULE_STATUS,default=1);
    Location=models.ForeignKey(Locations,on_delete=models.SET_NULL,null=True);
    RetentionDays=SmallIntegerField(verbose_name='Expire at',help_text='Total age of backup file',null=False);
    FileTag=models.CharField(help_text="Add tag to filename ultil remains on this location",max_length=40,null=True,blank=True);
    ZipFile=models.BooleanField(default=False, help_text='Compress backup file on arrival ',verbose_name='Compress file?')
    ZipFormat= models.SmallIntegerField(choices=COMPRESS_FORMAT,default=1);
    
    class Meta:
        table_name='backup_rotationrules'
        verbose_name_plural = "Rotation rules"
        ordering = ['Job', 'Order']

    def __str__(self):
        return  self.RuleName 
