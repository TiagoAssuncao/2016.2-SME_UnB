# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-25 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transductor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol_type', models.CharField(max_length=50)),
                ('port', models.IntegerField(default=1001)),
                ('timeout', models.FloatField(default=30.0)),
                ('transductor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transductor.EnergyTransductor')),
            ],
        ),
    ]
