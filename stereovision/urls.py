from django.urls import path
from . import views

app_name = 'stereovision'

urlpatterns = [
    path('', views.main, name='main'),    
    path('left/', views.left, name='left'),    
    path('right/', views.right, name='right'),    
    path('sshot/', views.sshot, name='sshot'),
    path('userdata_update/', views.userdata_update, name="userdata_update"),    
    path('userdata_delete/', views.userdata_delete, name="userdata_delete"),   

]
