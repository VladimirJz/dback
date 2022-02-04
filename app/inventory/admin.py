from django.contrib import admin
from app.inventory.models import Issues, IssuesType, ItemCategory,Item, ItemCondition,ItemStatus, Location
# Register your models here.
admin.site.register(Item)
admin.site.register(ItemStatus)
admin.site.register(ItemCategory)
admin.site.register(ItemCondition)
admin.site.register(Location)
admin.site.register(IssuesType)
admin.site.register(Issues)

