from django.contrib import admin
from .models import Rooms,Property,Tenant,TenentProfileVerify,Dues
# Register your models here.
admin.site.register(Rooms)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(TenentProfileVerify)
admin.site.register(Dues)