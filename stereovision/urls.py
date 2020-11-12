from django.urls import path
from . import views

app_name = 'stereovision'

urlpatterns = [
    path('', views.init, name='init'),
    path('main/', views.main, name='main'),   
    path('left/', views.left, name='left'),    
    path('right/', views.right, name='right'),    
    path('sshot/', views.sshot, name='sshot'),
    path('userdata_update/', views.userdata_update, name="userdata_update"),    
    path('userdata_delete/', views.userdata_delete, name="userdata_delete"),  
    path('setting/', views.setting, name="setting"),
    path('main/setting/', views.setting, name="setting"), #only use javascript location.href

    #Streaming Path
    path('video_left', views.video_left, name='video_left'),
    path('video_right', views.video_right, name='video_right'),
]
