# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('status', models.IntegerField(blank=True)),
                ('is_current', models.BooleanField()),
                ('create_time', models.DateTimeField(blank=True)),
            ],
        ),
    ]
