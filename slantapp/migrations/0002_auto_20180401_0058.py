# Generated by Django 2.0.3 on 2018-04-01 04:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slantapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_name', models.CharField(max_length=250)),
                ('publication_logo', models.ImageField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='publication',
        ),
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(default=datetime.date(1900, 1, 1)),
        ),
        migrations.AddField(
            model_name='article',
            name='issue',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='slantapp.Issue'),
        ),
        migrations.AddField(
            model_name='issue',
            name='date',
            field=models.DateField(default=datetime.date(1900, 1, 1)),
        ),
        migrations.AddField(
            model_name='article',
            name='publication_name',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='slantapp.Publication'),
        ),
    ]
