# Generated by Django 3.2.5 on 2022-03-28 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0009_auto_20220206_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sms',
            name='sent_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
