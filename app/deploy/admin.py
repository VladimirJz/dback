from django.contrib import admin
from app.deploy.models import Jobs,JobScripts,TableFilters


# Register your models here.
admin.site.register(Jobs)
admin.site.register(JobScripts)
admin.site.register(TableFilters)