# Generated by Django 3.1.2 on 2020-11-16 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CameraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.IntegerField()),
                ('camera_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CameraList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_index', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PreviewCamera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_left', models.PositiveIntegerField()),
                ('camera_right', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TargetImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_image_byte', models.BinaryField()),
                ('target_image_img', models.ImageField(upload_to='')),
                ('target_point_x1', models.IntegerField(null=None)),
                ('target_point_y1', models.IntegerField(null=None)),
                ('target_point_x2', models.IntegerField(null=None)),
                ('target_point_y2', models.IntegerField(null=None)),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_left_camera', models.IntegerField(default=0)),
                ('user_right_camera', models.IntegerField(default=1)),
                ('user_distance', models.IntegerField(default=100)),
                ('user_width', models.PositiveIntegerField(default=1280)),
                ('user_height', models.PositiveIntegerField(default=960)),
            ],
        ),
    ]
