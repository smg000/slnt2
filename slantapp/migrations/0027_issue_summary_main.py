# Generated by Django 2.0.4 on 2018-05-28 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slantapp', '0026_auto_20180517_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='summary_main',
            field=models.TextField(blank=True, default='', help_text='Add short summary of the topic.', null=True),
        ),
    ]
