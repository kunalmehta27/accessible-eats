# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0002_remove_review_has_space'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='has_space',
            field=models.BooleanField(default=0, help_text=b'6. Is there enough space for wheelchairs to navigate the floor of the restaurant?'),
            preserve_default=False,
        ),
    ]
