# Generated by Django 3.2.8 on 2021-10-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('krules_djangoapps_procevents', '0002_auto_20210607_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processingevent',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
