# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('logger_name', models.CharField(max_length=100)),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'NotSet'), (20, 'Info'), (30, 'Warning'), (10, 'Debug'), (40, 'Error'), (50, 'Fatal')], default=40, db_index=True)),
                ('msg', models.TextField()),
                ('trace', models.TextField(null=True, blank=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-create_datetime',),
            },
            bases=(models.Model,),
        ),
    ]
