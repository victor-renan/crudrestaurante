# Generated by Django 4.1.4 on 2023-01-09 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_encomenda'),
    ]

    operations = [
        migrations.AddField(
            model_name='encomenda',
            name='quantidade',
            field=models.IntegerField(default=1),
        ),
    ]
