from django.db import models

# Create your models here.
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, DecimalField, IntegerField
from django.db.models.fields.related import ForeignKey

from app.catalog.models import Tables



class TablesDetail(models.Model):
    Table=models.OneToOneField(Tables,on_delete=models.CASCADE,primary_key=True,related_name='DetailOf')
    CurrentDate=DateField(help_text="Update date info")
    LastAccess =DateField(null=True,help_text="Lastest table use date")
    DataSizeMB=DecimalField(max_digits=12,decimal_places=2,help_text='Data size storage')
    IndexSizeMB=DecimalField(max_digits=12,decimal_places=2,help_text='Index size storage')
    RowsNum=IntegerField(help_text='Number of Rows allocated')
    FKeysNum=IntegerField(help_text='Number of ForeingKeys')
    IndexNum=IntegerField(help_text='Number of Indexes')
    IndexReads=IntegerField(help_text='Index Reads')
    IndexUpdates=IntegerField(help_text='Index updates')
