from django.db import models

class Userdata(models.Model):
    user_left_camera = models.IntegerField(default=0)
    user_right_camera = models.IntegerField(default=1)
    user_distance = models.IntegerField(null=False, default=100)
    user_width = models.PositiveIntegerField(null=False, default=1280)
    user_height = models.PositiveIntegerField(null=False, default=960)

class TargetImage(models.Model):
    target_bytes = models.BinaryField(null=False)
    target_image = models.ImageField()
    target_point_x1 = models.IntegerField(null=None)
    target_point_y1 = models.IntegerField(null=None)
    target_point_x2 = models.IntegerField(null=None)
    target_point_y2 = models.IntegerField(null=None)

class CameraList(models.Model):
    camera_index = models.PositiveIntegerField(null=False)

class PreviewCamera(models.Model):
    camera_left = models.PositiveIntegerField(null=False)
    camera_right = models.PositiveIntegerField(null=False)