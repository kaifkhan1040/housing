from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('tenantverify/<str:id>',views.tenantverify,name='tenantverify'),

]