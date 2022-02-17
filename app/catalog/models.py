from django.db import models

# Create your models here.


from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField
from django.db.models.fields.related import ForeignKey

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
        table_name='catalog_servers'
        verbose_name_plural = "Servers"


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
        table_name='catalog_databases'
        verbose_name_plural = "Databases"


class TableCategory(models.Model):
    Category=CharField(max_length=40,help_text='Object Bussines Category')
    def __str__(self):
        return self.Category
    class Meta:
        table_name='catalog_tablecategory'



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
        table_name='catalog_tables'
        verbose_name_plural = "Tables"




