# Generated by Django 3.1.2 on 2020-11-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stereovision', '0010_auto_20201117_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetimage',
            name='target_bytes',
            field=models.BinaryField(),
        ),
    ]