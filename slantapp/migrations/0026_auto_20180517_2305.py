# Generated by Django 2.0.4 on 2018-05-18 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slantapp', '0025_auto_20180514_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='summary_left',
            field=models.TextField(blank=True, default='', help_text='Add summary of the left.', null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='summary_right',
            field=models.TextField(blank=True, default='', help_text='Add summary of the right.', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='url_blacklist',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
