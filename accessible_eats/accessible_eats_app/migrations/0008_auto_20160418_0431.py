# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accessible_eats_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0007_auto_20160418_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image1',
            field=models.FileField(help_text=b'(Optional) Upload image of accessibile features:', null=True, upload_to=accessible_eats_app.models.update_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='image2',
            field=models.FileField(help_text=b'(Optional) Upload additional image:', null=True, upload_to=accessible_eats_app.models.update_filename, blank=True),
        ),
    ]
