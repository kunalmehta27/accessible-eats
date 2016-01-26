# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessible_eats_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifiedReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessible', models.BooleanField(default=False, help_text=b'Accessibility')),
                ('name', models.CharField(help_text=b'Accessibility', max_length=255)),
                ('title', models.CharField(help_text=b'Title of Applier', max_length=255)),
                ('email', models.EmailField(help_text=b'Email of Applier', max_length=254)),
                ('application', models.TextField(help_text=b'Accessibility Application')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='verified',
            field=models.BooleanField(default=False, help_text=b'Whether the accessibility rating has been verified by restaurant.'),
        ),
        migrations.AddField(
            model_name='verifiedreview',
            name='restaurant',
            field=models.OneToOneField(related_name='verifiedreview', to='accessible_eats_app.Restaurant', help_text=b'O2O field to restaurant'),
        ),
    ]
