# Generated by Django 2.0.4 on 2018-04-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slantapp', '0004_auto_20180404_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='display',
            field=models.BooleanField(default=False),
        ),
    ]
