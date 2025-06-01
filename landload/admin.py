from django.contrib import admin
from .models import Rooms,Property,Tenant
# Register your models here.
admin.site.register(Rooms)
admin.site.register(Property)
admin.site.register(Tenant)