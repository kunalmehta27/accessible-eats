# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='has_space',
        ),
    ]
