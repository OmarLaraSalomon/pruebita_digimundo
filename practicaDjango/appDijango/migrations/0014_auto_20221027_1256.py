# Generated by Django 3.2.10 on 2022-10-27 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appDijango', '0013_lineapedido_pedido'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineapedido',
            old_name='pedido_id',
            new_name='pedido',
        ),
        migrations.RenameField(
            model_name='lineapedido',
            old_name='producto_id',
            new_name='producto',
        ),
    ]
