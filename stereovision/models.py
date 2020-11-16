from django.db import models

class CameraInfo(models.Model):
    camera_id = models.IntegerField(null=False)
    camera_name = models.CharField(max_length=200, null=False)

    def __str__(self):
        _id = str(self.camera_id)
        _output = _id + ": " + self.camera_name
        return _output

class Userdata(models.Model):
    user_left_camera = models.IntegerField(default=0)
    user_right_camera = models.IntegerField(default=1)
    user_distance = models.IntegerField(null=False, default=100)
    user_width = models.PositiveIntegerField(null=False, default=1280)
    user_height = models.PositiveIntegerField(null=False, default=960)

    def __str__(self):
        _left = "left: " + str(self.user_left_camera)
        _right = "right: " + str(self.user_left_camera)
        _distance = "distance: " + str(self.user_distance)
        _resolution = "resolution: " + str(self.user_width) + "x" + str(self.user_height)
        _output = "(" + _left + " " + _right + " " + _distance + " " + _resolution + ")"
        return _output

class TargetImage(models.Model):
    target_image_byte = models.BinaryField(null=False)
    target_point_x1 = models.IntegerField(null=None)
    target_point_y1 = models.IntegerField(null=None)
    target_point_x2 = models.IntegerField(null=None)
    target_point_y2 = models.IntegerField(null=None)

class CameraList(models.Model):
    camera_index = models.PositiveIntegerField(null=False)

class PreviewCamera(models.Model):
    camera_left = models.PositiveIntegerField(null=False)
    camera_right = models.PositiveIntegerField(null=False)