# Generated by Django 3.1.2 on 2020-11-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stereovision', '0006_delete_camerainfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetimage',
            name='target_name',
        ),
        migrations.AddField(
            model_name='targetimage',
            name='target_image_real',
            field=models.ImageField(default=None, upload_to='media'),
        ),
    ]