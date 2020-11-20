from django.urls import path
from . import views

app_name = 'stereovision'

urlpatterns = [
    path('', views.init, name='init'),
    path('main/', views.main, name='main'),   
    path('camera_preview/', views.camera_preview, name="camera_preview"), 
    path('userdata_update/', views.userdata_update, name="userdata_update"),    
    path('setting/', views.setting, name="setting"),
    path('main/setting/', views.setting, name="setting"),
    path('border_selection/', views.border_selection, name="border_selection"),
    path('target_table_check/', views.target_table_check, name="target_table_check"),
    path('target_table_delete/', views.target_table_delete, name="target_table_delete"),

    #Streaming Path
    path('video_left', views.video_left, name='video_left'),
    path('video_right', views.video_right, name='video_right'),

    path('pre_video_left', views.pre_video_left, name='pre_video_left'),
    path('pre_video_right', views.pre_video_right, name='pre_video_right'),
]
