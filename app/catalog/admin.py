from django.contrib import admin

from app.catalog.models import DataBases,Servers,TableCategory,Tables,Credentials

# Register your models here.
admin.site.register(Servers)
admin.site.register(Tables)
admin.site.register(TableCategory)
admin.site.register(DataBases)
admin.site.register(Credentials)


