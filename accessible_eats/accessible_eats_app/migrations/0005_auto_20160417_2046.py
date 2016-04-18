# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0004_auto_20160301_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='has_entrances',
            field=models.BooleanField(help_text=b'3. Does the restaurant have wide enough entrances (approx. 32in) to the restaurant and bathrooms that are easy to open?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_parking',
            field=models.BooleanField(help_text=b'2. Does the restaurant have designated van accessible parking?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_ramp',
            field=models.BooleanField(help_text=b'4. Is there a ramp, walkway or other device that leads to the restaurant from the parking lot?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_space',
            field=models.BooleanField(help_text=b'5. Is there enough space for wheelchairs to navigate and utilize all the tables and the floor of the restaurant?'),
        ),
    ]
