# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiApi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('project_id', models.IntegerField(null=True, blank=True)),
                ('api_http_type', models.IntegerField(null=True, blank=True)),
                ('api_url', models.CharField(max_length=500, null=True, blank=True)),
                ('url_list', models.TextField(null=True, blank=True)),
                ('api_domain', models.CharField(max_length=100, null=True, blank=True)),
                ('api_method', models.IntegerField(null=True, blank=True)),
                ('api_headers', models.TextField(null=True, blank=True)),
                ('api_body_type', models.IntegerField(null=True, blank=True)),
                ('api_body_value', models.TextField(null=True, blank=True)),
                ('api_expect_result', models.TextField(null=True, blank=True)),
                ('api_real_result', models.TextField(null=True, blank=True)),
                ('api_is_success', models.IntegerField(null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('creater', models.IntegerField(null=True, blank=True)),
                ('create_time', models.DateTimeField(null=True, blank=True)),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('last_execute_time', models.DateTimeField(null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
            ],
        ),
    ]
