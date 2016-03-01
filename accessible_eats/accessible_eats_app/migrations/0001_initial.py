# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
                ('yelp_id', models.CharField(help_text=b'Yelp ID', unique=True, max_length=255)),
                ('name', models.CharField(help_text=b'Name of Restaurant', max_length=255)),
                ('is_closed', models.BooleanField(default=False, help_text=b'Whether business has been closed permanently.')),
                ('snippet', models.CharField(help_text=b'Snippet about the restaurant.', max_length=255)),
                ('image_url', models.URLField(help_text=b'Image URL from Yelp')),
                ('phone', models.CharField(help_text=b'Formatted phone number for backend', max_length=20)),
                ('display_phone', models.CharField(help_text=b'Display phone number for HTML', max_length=30)),
                ('url', models.URLField(help_text=b'Yelp URL for the page')),
                ('rating', models.FloatField(help_text=b'Yelp Rating')),
                ('rating_img', models.URLField(help_text=b'Rating Image URL from Yelp')),
                ('display_address', models.TextField(help_text=b'Display Address for Restaurant')),
                ('city', models.CharField(help_text=b'City', max_length=255)),
                ('state', models.CharField(max_length=2, choices=[(b'AK', b'Alaska'), (b'AL', b'Alabama'), (b'AR', b'Arkansas'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DC', b'District of Columbia'), (b'DE', b'Delaware'), (b'DK', b'Dakota Territory'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'IA', b'Iowa'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'MA', b'Massachusetts'), (b'MD', b'Maryland'), (b'ME', b'Maine'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MO', b'Missouri'), (b'MP', b'Northern Mariana Islands'), (b'MS', b'Mississippi'), (b'MT', b'Montana'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'NE', b'Nebraska'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NV', b'Nevada'), (b'NY', b'New York'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OL', b'Territory of Orleans'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PI', b'Philippines Territory/Commonwealth'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VA', b'Virginia'), (b'VI', b'Virgin Islands'), (b'VT', b'Vermont'), (b'WA', b'Washington'), (b'WI', b'Wisconsin'), (b'WV', b'West Virginia'), (b'WY', b'Wyoming')])),
                ('zip_code', models.CharField(help_text=b'Zip code', max_length=10)),
                ('latitude', models.FloatField(help_text=b'Latitude')),
                ('longitude', models.FloatField(help_text=b'Longitude')),
                ('categories', models.ManyToManyField(help_text=b'Categories that the restaurant belongs to', to='accessible_eats_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_accessible_bathroom', models.BooleanField(help_text=b'1. Does the location have accessible bathrooms for both sexes, with handrails and enough room for wheelchairs?')),
                ('has_elevator', models.BooleanField(help_text=b'2. Does the restaurant have accessible access to all parts of the restaurant? (Elevators, if necessary)')),
                ('has_parking', models.BooleanField(help_text=b'3. Does the restaurant have designated accessible parking?')),
                ('has_entrances', models.BooleanField(help_text=b'4. Does the restaurant have wide enough entrances (approx. 32in) to the restaurant and bathrooms?')),
                ('has_ramp', models.BooleanField(help_text=b'5. Is there a ramp that leads to the restaurant from the parking lot?')),
                ('has_space', models.BooleanField(help_text=b'6. Is there enough space for wheelchairs to navigate the floor of the restaurant?')),
                ('comments', models.TextField(help_text=b'Additional optional comments', null=True, blank=True)),
                ('restaurant', models.ForeignKey(related_name='reviews', to='accessible_eats_app.Restaurant', help_text=b'Foreign key to restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewedTweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(max_length=255)),
            ],
        ),
    ]
