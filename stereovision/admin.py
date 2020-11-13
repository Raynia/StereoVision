from django.contrib import admin
from .models import CameraInfo, Userdata, TargetImage, CameraList
# Register your models here.

admin.site.register(CameraInfo)
admin.site.register(Userdata)
admin.site.register(TargetImage)
admin.site.register(CameraList)