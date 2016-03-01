from django.db import models
from types import State
from django.forms import ModelForm, TextInput, Textarea, ValidationError
import json
from collections import Counter

class Constants:
    review_score_values = {'has_accessible_bathroom':3, 'has_parking':2, 'has_space':1, 'has_ramp':2, 'has_entrances':2}
    max_score = sum(review_score_values.values())
    review_boolean_fields = ['has_accessible_bathroom', 'has_parking', 'has_space', 'has_ramp', 'has_entrances']
    filter_fields = {'has_accessible_bathroom':'Accessible Bathrooms', 'has_parking':'Parking', 'has_ramp':'Ramps', 'has_entrances':'Wide Entrances', 'has_space':'Floor Space'}

class Category(models.Model):
    name = models.CharField(max_length=255, help_text="Name of Category")
    slug = models.CharField(max_length=255, help_text="Category slug")


class Restaurant(models.Model):
    yelp_id = models.CharField(max_length=255, help_text="Yelp ID", unique=True)
    name = models.CharField(max_length=255, help_text="Name of Restaurant")
    is_closed = models.BooleanField(default=False, help_text="Whether business has been closed permanently.")
    snippet = models.CharField(max_length=255, help_text="Snippet about the restaurant.")

    image_url = models.URLField(help_text="Image URL from Yelp")
    phone = models.CharField(max_length=20, help_text="Formatted phone number for backend")
    display_phone = models.CharField(max_length = 30, help_text="Display phone number for HTML")
    url = models.URLField(help_text="Yelp URL for the page")

    review_count = models.IntegerField(help_text="Number of reviews.", null=True)
    categories = models.ManyToManyField(Category, help_text="Categories that the restaurant belongs to")
    rating = models.FloatField(help_text="Yelp Rating")
    rating_img = models.URLField(help_text="Rating Image URL from Yelp")

    display_address = models.TextField(help_text="Display Address for Restaurant")
    city = models.CharField(max_length=255, help_text="City")
    state = models.CharField(choices=sorted(State, key = lambda x: x[0]), max_length=2)
    zip_code = models.CharField(max_length=10, help_text="Zip code")

    latitude = models.FloatField(help_text="Latitude")
    longitude = models.FloatField(help_text="Longitude")

    def __unicode__(self):
        return self.name

    def accessible_rating(self):
        score = 0
        for field in Constants.review_boolean_fields:
            if self.aggregate_rating(field):
                score += Constants.review_score_values[field]
        return score

    def max_rating(self):
        return Constants.max_score

    def aggregate_rating(self, attr):
        reviews = self.reviews.all()
        if reviews.count() == 0:
            return False
        else:
            values = Counter(reviews.values_list(attr, flat=True))
            if values[True] >= values[False]:
                return True
            else:
                return False
            return True


    def accessibility_data(self):
        accessibility_data = []
        for field in Constants.review_boolean_fields:
            if self.aggregate_rating(field):
                accessibility_data.append(Constants.filter_fields[field])
        if len(accessibility_data) == 0:
            return "None"
        elif len(accessibility_data) == 1:
            return accessibility_data[0]
        else:
            return ", ".join(accessibility_data)

    def address(self):
        return self.display_address + '<br>' + self.city + ', ' + self.state + ' ' + self.zip_code


    def address_oneline(self):
        return self.display_address + ', ' + self.city + ', ' + self.state + ' ' + self.zip_code

    def categories_list(self):
        categories = self.categories.all().values_list('name', flat=True)
        string = ', '.join(categories)
        return string

    def accessible_rating_color(self):
        if self.accessible_rating() >= 7:
            return 'text-success'
        else:
            return 'text-danger'

    def review_count(self):
        count = self.reviews.all().count()
        if count == 1:
            return str(count) + ' review'
        else:
            return str(count) + ' reviews'

    def has_review_text(self):
        reviews = self.reviews.all().exclude(comments = None)
        if reviews.count() > 0:
            return True
        else:
            return False


class Review(models.Model):
    has_accessible_bathroom = models.BooleanField(blank=True, help_text="1. Does the location have accessible bathrooms for both sexes, with handrails and enough room for wheelchairs?")
    has_parking = models.BooleanField(blank=True, help_text="2. Does the restaurant have designated accessible parking?")
    has_entrances = models.BooleanField(blank=True, help_text="3. Does the restaurant have wide enough entrances (approx. 32in) to the restaurant and bathrooms?")
    has_ramp = models.BooleanField(blank=True, help_text="4. Is there a ramp, walkway or other device that leads to the restaurant from the parking lot?")
    has_space = models.BooleanField(blank=True, help_text="5. Is there enough space for wheelchairs to navigate and utilize all the tables and the floor of the restaurant?")
    restaurant = models.ForeignKey(Restaurant, related_name="reviews", help_text="Foreign key to restaurant")
    comments = models.TextField(null=True, blank=True, help_text="Additional optional comments")


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'restaurant': TextInput(attrs={'class':'form-control'}),
            'comments': Textarea(attrs={'class':'form-control', 'placeholder':'Please provide any additional information you wish here.'})
        }

    def clean(self):
        from helpers import text_to_object
        super(ReviewForm, self).clean()
        restaurant_errors = json.loads(self._errors.as_json())['restaurant'][0]
        if restaurant_errors['code'] == 'required':
            return self.cleaned_data
        elif restaurant_errors['code'] == 'invalid_choice':
            restaurant_obj = text_to_object(self.data['restaurant'])
            if restaurant_obj:
                del self._errors['restaurant']
                self.cleaned_data['restaurant'] = restaurant_obj
            else:
                message = "No restaurant found. Please try again."
                error = ValidationError(message, code='invalid_choice')
                del self._errors['restaurant']
                self.add_error('restaurant', error)
            return self.cleaned_data

class SurveyForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'comments': Textarea(attrs={'class':'form-control', 'placeholder':'Please provide any additional information you wish here.'})
        }


class ReviewedTweet(models.Model):
    tweet_id = models.CharField(max_length=255)


