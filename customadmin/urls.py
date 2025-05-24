from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('landload',views.landload,name='landload'),
    path('add_landload',views.add_landload,name='add_landload'),
    path('update_landload/<int:id>',views.add_landload,name='update_landload'),
    path('delete_landload/<int:id>',views.delete_landload,name='delete_landload'),

]