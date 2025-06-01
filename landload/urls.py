from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('listing',views.listing,name='listing'),
    path('listing-add',views.listing_add,name='listing_add'),
    path('listing-view/<int:id>/',views.listing_view,name='listing_view'),
    path('listing-update/<int:id>/',views.listing_update,name='listing_update'),
    path('room/<int:id>/',views.room,name='room'),
    path('deactivate_property/<int:pk>/',views.deactivate_property,name='deactivate_property'),

    path('tenant',views.tenant,name='tenant'),
    path('tenant-add',views.tenant_add,name='tenant_add'),
    path('tenant-view/<int:id>/',views.tenant_view,name='tenant_view'),
    path('tenant-update/<int:id>/',views.tenant_update,name='tenant_update'),
    
    path('get_room',views.get_room,name='get_room'),
]