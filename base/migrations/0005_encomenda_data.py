# Generated by Django 4.1.4 on 2023-01-10 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_encomenda_quantidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='encomenda',
            name='data',
            field=models.DateField(auto_now=True),
        ),
    ]
