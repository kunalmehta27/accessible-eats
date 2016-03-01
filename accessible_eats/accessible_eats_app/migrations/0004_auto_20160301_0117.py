# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0003_review_has_space'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='has_elevator',
        ),
        migrations.AlterField(
            model_name='review',
            name='has_entrances',
            field=models.BooleanField(help_text=b'3. Does the restaurant have wide enough entrances (approx. 32in) to the restaurant and bathrooms?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_parking',
            field=models.BooleanField(help_text=b'2. Does the restaurant have designated accessible parking?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_ramp',
            field=models.BooleanField(help_text=b'4. Is there a ramp that leads to the restaurant from the parking lot?'),
        ),
        migrations.AlterField(
            model_name='review',
            name='has_space',
            field=models.BooleanField(help_text=b'5. Is there enough space for wheelchairs to navigate the floor of the restaurant?'),
        ),
    ]
