from django.db import models

#Camera 클래스
class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    camera_name = models.CharField(max_length=200)
    frame = models.PositiveIntegerField(default=0)
    resolution_width = models.PositiveIntegerField(default=0)
    resolution_height = models.PositiveIntegerField(default=0)
    def __str__(self):
        _id = str(self.id)
        _output = _id + ": " + self.camera_name
        return _output

class Userdata(models.Model):
    id = models.AutoField(primary_key=True)
    left = models.IntegerField(default=0)
    right = models.IntegerField(default=1)
    distance = models.IntegerField(default=100)
    user_width = models.PositiveIntegerField(default=640)
    user_height = models.PositiveIntegerField(default=480)
    def __str__(self):
        _id = str(self.id)
        _left = "left: " + str(self.left)
        _right = "right: " + str(self.right)
        _distance = "distance: " + str(self.distance)
        _resolution = "resolution: " + str(self.user_width) + "x" + str(self.user_height)
        _output = _id + ": (" + _left + " " + _right + " " + _distance + " " + _resolution + ")"
        return _output
