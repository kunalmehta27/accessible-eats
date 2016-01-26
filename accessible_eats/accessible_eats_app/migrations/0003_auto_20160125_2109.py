# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0002_auto_20160118_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='yelp_id',
            field=models.CharField(help_text=b'Yelp ID', unique=True, max_length=255),
        ),
    ]
