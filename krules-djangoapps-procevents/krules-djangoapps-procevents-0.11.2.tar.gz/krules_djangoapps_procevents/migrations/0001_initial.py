# Generated by Django 3.2.3 on 2021-05-31 15:03

from django.db import migrations, models
import krules_djangoapps_common.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('event_info', krules_djangoapps_common.fields.EmptyObjectJSONField(default=dict)),
                ('payload', krules_djangoapps_common.fields.EmptyObjectJSONField(default=dict)),
                ('time', models.DateTimeField()),
                ('filters', krules_djangoapps_common.fields.EmptyObjectJSONField(default=list)),
                ('processing', krules_djangoapps_common.fields.EmptyObjectJSONField(default=list)),
                ('got_errors', models.BooleanField()),
                ('passed', models.BooleanField()),
                ('source', models.CharField(max_length=255)),
                ('origin_id', models.CharField(max_length=255)),
            ],
        ),
    ]
