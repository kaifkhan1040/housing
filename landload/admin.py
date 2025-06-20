from django.contrib import admin
from .models import Rooms,Property,Tenant,TenentProfileVerify,Dues,Country,\
    FinancialBreakdown,FinancialOtherModel,PropertyImage
# Register your models here.
admin.site.register(Rooms)
admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(TenentProfileVerify)
admin.site.register(Dues)
admin.site.register(Country)
admin.site.register(FinancialBreakdown)
admin.site.register(FinancialOtherModel)
admin.site.register(PropertyImage)