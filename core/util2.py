
class TableDetails(models.Model):
    Updated=DateField(help_text='Details update on')
    Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)
    LastUse=DateField(help_text='Accessed on')
    NumRows=IntegerField(help_text='Number of Rows')
    DataSizeMb=DecimalField(help_text='Data Storage')
    NumIndex=IntegerField(help_text='Number of Indexes')
    IndexSizeMb=DecimalField(help_text='Index Storage')
    IndexReads=IntegerField(help_text='Number of Index reads')
    IndexUpdates=IntegerField(help_text='Number of Index Updates')

class TableHistory(models.Model):
    Date=DateField(help_text='History date')
    Table=ForeignKey(Tables,on_delete=models.SET_NULL,null=True)
    LastUse=DateField(help_text='Accessed on')
    NumRows=IntegerField(help_text='Number of Rows')
    DataSizeMb=DecimalField(help_text='Data Storage')
    NumIndex=IntegerField(help_text='Number of Indexes')
    IndexSizeMb=DecimalField(help_text='Index Storage')
    IndexReads=IntegerField(help_text='Number of Index reads')
    IndexUpdates=IntegerField(help_text='Number of Index Updates')