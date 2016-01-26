from django.db import models
from types import State

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

	review_count = models.IntegerField(help_text="Number of reviews.")
	categories = models.ManyToManyField(Category, help_text="Categories that the restaurant belongs to")
	rating = models.FloatField(help_text="Yelp Rating")
	rating_img = models.URLField(help_text="Rating Image URL from Yelp")

	display_address = models.TextField(help_text="Display Address for Restaurant")
	city = models.CharField(max_length=255, help_text="City")
	state = models.CharField(choices=sorted(State, key = lambda x: x[0]), max_length=2)
	zip_code = models.CharField(max_length=10, help_text="Zip code")

	latitude = models.FloatField(help_text="Latitude")
	longitude = models.FloatField(help_text="Longitude")

	verified = models.BooleanField(default=False, help_text="Whether the accessibility rating has been verified by restaurant.")

	def __unicode__(self):
		return self.name

	def accessible_rating(self):
		reviews = self.reviews.all().count()
		accessible_reviews = self.reviews.all().filter(accessible=True).count()

		return round(float(accessible_reviews) / float(reviews) * 100, 0)


class AccessibleReview(models.Model):
	accessible = models.BooleanField(default=False)
	restaurant = models.ForeignKey(Restaurant, related_name="reviews", help_text="Foreign key to restaurant")


class VerifiedReview(models.Model):
	restaurant = models.OneToOneField(Restaurant, related_name="verifiedreview", help_text="O2O field to restaurant")
	accessible = models.BooleanField(default=False, help_text="Accessibility")
	name = models.CharField(max_length=255, help_text="Accessibility")
	title = models.CharField(max_length=255, help_text="Title of Applier")
	email = models.EmailField(help_text="Email of Applier")
	application = models.TextField(help_text="Accessibility Application")

