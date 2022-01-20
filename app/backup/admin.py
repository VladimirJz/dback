from django.contrib import admin

# Register your models here.


from app.backup.models import Backups,Locations,Jobs,Rotation,Status
# Register your models here.
admin.site.register(Backups)
admin.site.register(Locations)
admin.site.register(Jobs)
admin.site.register(Rotation)
admin.site.register(Status)



