# Generated by Django 3.2.10 on 2023-09-22 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appDijango', '0036_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='/appDijango/static/imgs/logo.jpg', null=True, upload_to=''),
        ),
    ]
