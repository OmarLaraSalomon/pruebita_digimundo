# Generated by Django 3.2.10 on 2023-09-21 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appDijango', '0031_auto_20230921_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosa',
            name='timestamp_modificacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
