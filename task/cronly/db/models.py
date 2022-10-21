import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


# Catalog

from datetime import date
from django.db.models.fields import CharField, DateField, DecimalField, SmallIntegerField,IntegerField
from django.db.models.fields.related import ForeignKey
from datetime import datetime, timedelta
from dateutil import parser

# Create your models here.
# Create your models here.
class Servers(models.Model):
    Server=CharField(max_length=50,help_text='Server name')
    Host=CharField(max_length=50,help_text='IP or Hostname')
    Instance=CharField(max_length=50,help_text='Instance Name')
    Port=IntegerField(help_text='Port Number')
    DBMS_TYPES = [(1, 'MS SQLServer'),(2,'MySQL/MariaDB'),(3, 'PostgreSQL')];
    Type= models.SmallIntegerField(choices=DBMS_TYPES,default=1,help_text='Type of Server');
    SERVER_ENV = [(1, 'Production'),(2,'QA'),(3, 'Development')];
    Environment =models.SmallIntegerField(choices=SERVER_ENV,default=1,help_text='Database Enviroment')
    SERVER_STATUS = [(1, 'Active'),(2,'Inactive'),(3,'Inaccessible')];
    Status= models.SmallIntegerField(choices=SERVER_STATUS,default=1,help_text='Server status');
    def __str__(self):
        return self.Server
    def get_absolute_url(self):
        return "/servers/update/%i" % self.id
    class Meta:
        db_table="catalog_servers"
        verbose_name_plural = "Servers"

class Credentials(models.Model):
    Server=models.ForeignKey(Servers,on_delete=models.SET_NULL,null=True, related_name='his_credentials')
    User=models.CharField(max_length=30, help_text='User name', verbose_name='User')
    Pass=models.CharField(max_length=30, help_text='Password',verbose_name='Password')

    class Meta:
        db_table='catalog_secures'
        verbose_name_plural = "Credentials"
    
class DataBases(models.Model):
    Database=CharField(max_length=50,help_text='Database Name')
    FriendlyName=CharField(max_length=50,help_text='Friendly Name',null=True)
    Description=CharField(max_length=200,help_text='Database description',null=True)
    CreateDate=DateField(help_text='Create date',default=date.today)
    DataSizeMB=IntegerField(help_text='Data size storage',default=0)
    IndexSizeMB=IntegerField(help_text='Index size storage',default=0)
    TablesNum=IntegerField(help_text='Number of tables',default=0)
    ViewsNum=IntegerField(help_text='Number of views',default=0)
    RoutinesNum=IntegerField(help_text='Number of routines',default=0)
    Server=ForeignKey(Servers,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.FriendlyName + ' (' + self.Database + ')'
    
    class Meta:
        db_table='catalog_databases'
        verbose_name_plural = "Databases"


class TableCategory(models.Model):
    Category=CharField(max_length=40,help_text='Object Bussines Category')
    def __str__(self):
        return self.Category
    class Meta:
        db_table='catalog_tablecategory'



class Tables(models.Model):
    Schema=CharField(max_length=20,null=True,help_text='Schema Database')
    DataBase=ForeignKey(DataBases,on_delete=models.SET_NULL,null=True,related_name='TablesOf')
    Name=CharField(max_length=50,null=False,help_text='Database name')
    ObjectID=CharField(max_length=50,null=True,help_text='Internal SGDB ID')
    TableCategory=ForeignKey(TableCategory,on_delete=models.SET_NULL,null=True)
    CreateDate=DateField(help_text='Creation date')
    TABLE_STATUS = [(1, 'Active'),(2,'Offline'),(3, 'Deleted')];
    Status= models.SmallIntegerField(choices=TABLE_STATUS,default=1);
    def __str__(self):
        return self.Name

    class Meta:
        db_table='catalog_tables'
        verbose_name_plural = "Tables"




## backups ###




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
        db_table='backup_locations'
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
        db_table='backup_jobs'
        verbose_name_plural = "Jobs"


class JobSchedule(models.Model):
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True);
    SCHEDULE = [(1, 'Daily'),(2, 'Weekend'),];
    Schedule=models.SmallIntegerField(choices=SCHEDULE,default=1);
    
    def __str__(self):
        job=Jobs.objects.get(id=4)
        return job.JobName +' - '+ self.get_Schedule_display()
   
    class Meta:
        db_table='backup_schedules'
        verbose_name_plural="Schedule"




class Status(models.Model):
    Status=models.CharField(max_length=20,help_text='Status');
    Description=models.CharField(max_length=200,help_text='Status description',null=True,blank=True)
    
    def __str__(self):
        return self.Description
    class Meta:
        db_table='backup_status'
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
    Updated = models.DateTimeField(verbose_name='Updated on', auto_now=True)

    class Meta:
        db_table = "backup_files"
        verbose_name_plural = "Backups"

    def __str__(self):
            return self.FileName
    def days_old(self):
        today=date.today().strftime('%Y-%m-%d')
        backup_date=datetime.strftime(self.CreationDate,'%Y-%m-%d')
        today=parser.parse(today)
        backup_date=parser.parse(backup_date)  
        diff=today-backup_date
        days_old=(diff.days)
        return days_old
        

class RotationRules(models.Model):
    Job=models.ForeignKey(Jobs,on_delete=models.SET_NULL,null=True,related_name='his_rules');
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
        db_table='backup_rotationrules'
        verbose_name_plural = "Rotation rules"
        ordering = ['Job', 'Order']

    def __str__(self):
        return  self.RuleName +' - ' +  str(self.RetentionDays)

    def prev_rule(self):
        next_step=RotationRules.objects.filter(Order__gt=self.Order).order_by('Order')[:1]
        if(next_step):
            return next_step
        else:
            return None
        
    def next_rule(self):
        pass    


