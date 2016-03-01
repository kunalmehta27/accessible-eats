from django.shortcuts import render, HttpResponse
from .helpers import text_to_object, text_to_coordinate
from .models import *
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
import json, urllib
import numpy as np
import math
from django.views.decorators.csrf import csrf_exempt
from pyshorteners import Shortener
from django.core.mail import mail_admins


class BoundingBox(object):
    def __init__(self, *args, **kwargs):
        self.lat_min = None
        self.lon_min = None
        self.lat_max = None
        self.lon_max = None


def get_bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_miles):
    assert half_side_in_miles > 0
    assert latitude_in_degrees >= -180.0 and latitude_in_degrees  <= 180.0
    assert longitude_in_degrees >= -180.0 and longitude_in_degrees <= 180.0

    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius  = 6371.0
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_miles/radius
    lat_max = lat + half_side_in_miles/radius
    lon_min = lon - half_side_in_miles/parallel_radius
    lon_max = lon + half_side_in_miles/parallel_radius
    rad2deg = math.degrees

    box = BoundingBox()
    box.lat_min = rad2deg(lat_min)
    box.lon_min = rad2deg(lon_min)
    box.lat_max = rad2deg(lat_max)
    box.lon_max = rad2deg(lon_max)

    return (box)


def create_stars(num):
    if np.ceil(num) - num == 0.5:
        half_star = True
    else:
        half_star = False
    stars = ''
    for i in range(int(np.floor(num))):
        stars += '&#9733;'
    if half_star:
        stars += '&frac12;'
    return stars


def index(request):
    return render(request, "index.html", {})


def review(request):
    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "thanks.html", {})
        else:
            return render(request, "review.html", {'form':form})
        
    else:
        form = ReviewForm()
        return render(request, "review.html", {'form':form})


def search(request):
    restaurants = Restaurant.objects.all().values_list('name', flat=True)
    restaurants =[a.encode('utf8') for a in restaurants]
    restaurants = json.dumps(restaurants)

    categories = Category.objects.all().values_list('name', flat=True)
    categories = [a.encode('utf8') for a in categories]
    categories = json.dumps(categories)

    grades = np.arange(1, 5.5, 0.5)
    stars = []
    for grade in grades:
        if np.ceil(grade) - grade != 0.5:
            grade_append = int(grade)
            if grade_append == 1:
                grade_append = str(grade_append) + ' Star'
            else:
                grade_append = str(grade_append) + ' Stars'
        else:
            grade_append = str(grade) + ' Stars'
        stars.append([grade, grade_append, create_stars(grade)])

    ratings = range(1,11)
    max_rating = Constants.max_score

    fields = Constants.filter_fields
    json_fields = json.dumps(fields)

    return render(request, "search.html", {'restaurants':restaurants, 'categories':categories, 'stars':stars, 'ratings':ratings, 'max_rating':max_rating, 'fields':fields, 'json_fields':json_fields})


def searchresults(request, page_num, name, category, yelp_rating, ae_rating, filter_vals, lat, lng, location_name):
    restaurants = Restaurant.objects.all()
    restaurants = [a for a in restaurants if a.review_count() != '0 reviews']
    restaurants = Restaurant.objects.filter(id__in = [a.id for a in restaurants])

    filter_vals = json.loads(urllib.unquote(filter_vals))

    for field in filter_vals:
        if filter_vals[field]:
            restaurants = [a for a in restaurants if a.aggregate_rating(field)]
            restaurants = Restaurant.objects.filter(id__in = [a.id for a in restaurants])

    if name != '0':
        name = urllib.unquote(name)
        restaurants = restaurants.filter(name__icontains = name)

    if category != '0':
        category = urllib.unquote(category)
        restaurants = restaurants.filter(categories__name__iexact = category)

    if yelp_rating != '0':
        yelp_rating = float(yelp_rating)
        restaurants = restaurants.filter(rating__gte = yelp_rating)

    if ae_rating != '0':
        ae_rating = int(ae_rating)
        restaurants = [a for a in restaurants if a.accessible_rating() >= ae_rating]
        restaurants = Restaurant.objects.filter(id__in = [a.id for a in restaurants])

    if lat != '0' and lng != '0':
        box = get_bounding_box(float(lat), float(lng), 50)
        restaurants = Restaurant.objects.filter(latitude__lte = box.lat_max, latitude__gte = box.lat_min, longitude__lte = box.lon_max, longitude__gte = box.lon_min)

    if location_name != '0':
        location_name = urllib.unquote(location_name)
        lat, lng = text_to_coordinate(location_name)
        box = get_bounding_box(lat, lng, 50)
        restaurants = Restaurant.objects.filter(latitude__lte = box.lat_max, latitude__gte = box.lat_min, longitude__lte = box.lon_max, longitude__gte = box.lon_min)


    num_per_page = 3
    paginator = Paginator(restaurants, num_per_page)
    restaurants = paginator.page(page_num)
    return render(request, "restaurant_results.html", {'restaurants': restaurants, 'page_num': page_num, 'num_pages': paginator.num_pages})


def survey_only(request, restaurant_id):
    if request.POST:
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "thanks.html", {})
        else:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            return render(request, "review.html", {'form':form, 'restaurant_id':restaurant_id, 'restaurant':restaurant})
    else:
        form = SurveyForm(initial={'restaurant':restaurant_id})
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return render(request, 'survey_only.html', {'form':form, 'restaurant_id':restaurant_id, 'restaurant':restaurant})


@csrf_exempt
def text(request):
    error_msg = 'Sorry, we had a problem parsing your request. Please try again.'
    msg = request.POST.get('Body', '')
    restaurant_obj = text_to_object(msg)
    if restaurant_obj is None:
        response = error_msg
    else:
        url = 'http://' + request.META['HTTP_HOST'] + '/survey/' + str(restaurant_obj.id) + '/'
        response = "Thanks for using Accessible Eats. Fill out your survey for " + restaurant_obj.name + " at " + url + ". If this is not the restaurant you were looking for, please text us again with the restaurant name and general location."
    if msg.strip() == '' or restaurant_obj == None:
        twiml = '<Response><Message>' + error_msg + '</Message></Response>'
    else:
        twiml = '<Response><Message>' + response + '</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')


def resources(request):
    return render(request, "resources.html", {})


def custom_404(request):
    return render_to_response('404.html')


def custom_500(request):
    return render_to_response('500.html')

