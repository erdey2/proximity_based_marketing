# Generated by Django 5.1.7 on 2025-03-24 11:26

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('beacons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeaconMessage',
            fields=[
                ('message_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('image', 'image'), ('video', 'video'), ('text', 'text')], default='text', max_length=10)),
                ('sent_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('read_at', models.DateTimeField(null=True)),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='beacons.beacon')),
            ],
        ),
    ]
