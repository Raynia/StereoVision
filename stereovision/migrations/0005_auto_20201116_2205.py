# Generated by Django 3.1.2 on 2020-11-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stereovision', '0004_targetimage_target_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetimage',
            name='target_name',
            field=models.CharField(max_length=200),
        ),
    ]
