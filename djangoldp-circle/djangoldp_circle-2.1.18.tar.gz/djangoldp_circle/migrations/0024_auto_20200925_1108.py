# Generated by Django 2.2.16 on 2020-09-25 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_circle', '0023_auto_20200617_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_circles', to=settings.AUTH_USER_MODEL),
        ),
    ]
