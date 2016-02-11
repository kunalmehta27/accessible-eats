from django.shortcuts import render, HttpResponse
from .helpers import text_to_object
from .models import *
from django.db import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
import json, urllib
import numpy as np

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


def searchresults(request, page_num, name, category, yelp_rating, ae_rating, filter_vals):
    restaurants = Restaurant.objects.all()

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

    num_per_page = 3
    paginator = Paginator(restaurants, num_per_page)
    restaurants = paginator.page(page_num)
    return render(request, "restaurant_results.html", {'restaurants': restaurants, 'page_num': page_num, 'num_pages': paginator.num_pages})

