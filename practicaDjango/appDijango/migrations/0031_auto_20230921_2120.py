# Generated by Django 3.2.10 on 2023-09-21 21:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appDijango', '0030_datosa_modificaciones'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datosa',
            options={'ordering': ['-timestamp_modificacion']},
        ),
        migrations.RemoveField(
            model_name='datosa',
            name='modificaciones',
        ),
        migrations.AddField(
            model_name='datosa',
            name='direccion_anterior',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datosa',
            name='telefono_anterior',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datosa',
            name='timestamp_modificacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
