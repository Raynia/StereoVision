# Generated by Django 3.1.2 on 2020-11-17 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stereovision', '0008_auto_20201117_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetimage',
            name='target_image_real',
            field=models.ImageField(upload_to='media/stereovision'),
        ),
    ]
