# Generated by Django 2.0.4 on 2018-05-08 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slantapp', '0020_auto_20180507_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='prepend',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publication',
            name='regex',
            field=models.TextField(blank=True, null=True),
        ),
    ]
