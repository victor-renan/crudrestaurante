# Generated by Django 4.1.4 on 2023-01-22 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('system_admin', 'Pode modificar o cardapio'),)},
        ),
    ]
