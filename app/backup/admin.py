from django.contrib import admin

# Register your models here.


from app.backup.models import Backups, JobSchedule,Locations,Jobs,RotationRules,Status
# Register your models here.


class BackupsAdmin(admin.ModelAdmin):
    list_filter=('Location__LocationName','Status__Status')
    list_display=('FileName','Database','CreationDate','IsAvailable','Status','SizeMB','Location')
    def IsAvailable(self,obj):
        return obj.Status_id==1
    IsAvailable.boolean = True

class RotationRulesAdmin(admin.ModelAdmin):
    list_display=('Job','Order','RuleName','Location','RetentionDays')
  

admin.site.register(Backups,BackupsAdmin)
admin.site.register(Locations)
admin.site.register(Jobs)
admin.site.register(RotationRules,RotationRulesAdmin)
#admin.site.register(Status)
admin.site.register(JobSchedule)



