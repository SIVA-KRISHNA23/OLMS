from django.contrib import admin
from .models import Outing,Leave
# Register your models here.
class LeaveAdmin(admin.ModelAdmin):
    list_display=['user','start_date','end_date']
class OutingAdmin(admin.ModelAdmin):
    list_display=['user','out_time','in_time']

admin.site.register(Leave,LeaveAdmin)
admin.site.register(Outing,OutingAdmin)