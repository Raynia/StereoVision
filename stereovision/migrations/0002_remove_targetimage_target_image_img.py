# Generated by Django 3.1.2 on 2020-11-16 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stereovision', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetimage',
            name='target_image_img',
        ),
    ]
