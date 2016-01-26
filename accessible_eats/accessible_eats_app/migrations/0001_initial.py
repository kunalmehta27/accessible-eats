# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessibleReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of Category', max_length=255)),
                ('slug', models.CharField(help_text=b'Category slug', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yelp_id', models.CharField(help_text=b'Yelp ID', max_length=255)),
                ('name', models.CharField(help_text=b'Name of Restaurant', max_length=255)),
                ('is_closed', models.BooleanField(default=False, help_text=b'Whether business has been closed permanently.')),
                ('snippet', models.CharField(help_text=b'Snippet about the restaurant.', max_length=255)),
                ('image_url', models.URLField(help_text=b'Image URL from Yelp')),
                ('phone', models.CharField(help_text=b'Formatted phone number for backend', max_length=20)),
                ('display_phone', models.CharField(help_text=b'Display phone number for HTML', max_length=30)),
                ('url', models.URLField(help_text=b'Yelp URL for the page')),
                ('review_count', models.IntegerField(help_text=b'Number of reviews.')),
                ('rating', models.FloatField(help_text=b'Yelp Rating')),
                ('rating_img', models.URLField(help_text=b'Rating Image URL from Yelp')),
                ('display_address', models.TextField(help_text=b'Display Address for Restaurant')),
                ('city', models.CharField(help_text=b'City', max_length=255)),
                ('state_code', models.CharField(help_text=b'State code', max_length=3)),
                ('zip_code', models.CharField(help_text=b'Zip code', max_length=10)),
                ('latitude', models.FloatField(help_text=b'Latitude')),
                ('longitude', models.FloatField(help_text=b'Longitude')),
                ('categories', models.ManyToManyField(help_text=b'Categories that the restaurant belongs to', to='accessible_eats_app.Category')),
            ],
        ),
        migrations.AddField(
            model_name='accessiblereview',
            name='restaurant',
            field=models.ForeignKey(related_name='reviews', to='accessible_eats_app.Restaurant', help_text=b'Foreign key to restaurant'),
        ),
    ]
