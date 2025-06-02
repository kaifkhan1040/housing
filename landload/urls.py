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
    path('deactivate_tenant/<int:pk>/',views.deactivate_tenant,name='deactivate_tenant'),

    path('tenant',views.tenant,name='tenant'),
    path('tenant-add',views.tenant_add,name='tenant_add'),
    path('tenant-invite-add',views.tenant_invite_add,name='tenant_invite_add'),
    path('tenant-view/<int:id>/',views.tenant_view,name='tenant_view'),
    path('tenant-update/<int:id>/',views.tenant_update,name='tenant_update'),
    
    path('dues',views.dues,name='dues'),
    path('dues-add',views.dues_add,name='dues_add'),
    path('dues-view/<int:id>/',views.dues_view,name='dues_view'),
    path('dues-update/<int:id>/',views.dues_update,name='dues_update'),

    path('get_room',views.get_room,name='get_room'),
]