# Generated by Django 5.1.7 on 2025-03-24 11:26

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('beacon_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('minor', models.IntegerField(blank=True, default=0, null=True)),
                ('major', models.IntegerField(blank=True, default=0, null=True)),
                ('location_name', models.CharField(db_index=True, max_length=100)),
                ('signal_strength', models.FloatField(blank=True, null=True)),
                ('battery_status', models.FloatField(blank=True, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inactive', max_length=10)),
                ('latitude', models.FloatField(blank=True, default=9.145, null=True)),
                ('longitude', models.FloatField(blank=True, default=38.7525, null=True)),
            ],
        ),
    ]
