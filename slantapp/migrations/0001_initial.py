# Generated by Django 2.0.3 on 2018-03-31 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=250)),
                ('byline', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=250)),
                ('bias', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.CharField(max_length=100)),
            ],
        ),
    ]
