from accessible_eats_app.models import *
from yelpapi import YelpAPI
import urllib, urllib2
import json


GOOGLE_API_KEY = 'AIzaSyDnAkO8M2ykT71YBC0WmSfmZtEUhnoCN50'
yelp_api = YelpAPI('US2mtMpskJ36JSb_n6Uy-w', 'gtu09XfGR3FwC_Ar7LLYGEB-3EM', 'fIvJ3B48nF_Ro6QP5C-m6ptJOQHB5p7u', '8lApWweZlez8vmlBYQ5mNMW3pWI')

def text_to_coordinate(name):
    name = urllib.quote(name)
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' % (name, GOOGLE_API_KEY)
    page = urllib2.urlopen(url)
    data = page.read()
    obj = json.loads(data)
    obj = obj['results'][0]['geometry']['location']
    lat = float(obj['lat'])
    lng = float(obj['lng'])
    return lat, lng


def parse_google_places(name):
    name = urllib.quote(name)
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' % (name, GOOGLE_API_KEY)
    page = urllib2.urlopen(url)
    data = page.read()
    obj = json.loads(data)
    try:
        name = obj['results'][0]['name']
    except IndexError:
        return None, None
    address = obj['results'][0]['formatted_address']
    return name, address


def parse_yelp_obj(yelp_obj, db_obj):
    attr_list = [['yelp_id', 'id'], ['name', 'name'], ['is_closed', 'is_closed'], ['snippet','snippet_text'], ['image_url', 'image_url'], ['phone', 'phone'], ['display_phone', 'display_phone'], ['url', 'url'], ['review_count', 'review_count'], ['rating', 'rating'], ['rating_img', 'rating_img_url']]
    for attr in attr_list:
        setattr(db_obj, attr[0], yelp_obj[attr[1]])
    db_obj.display_address = yelp_obj['location']['display_address'][0]
    db_obj.city = yelp_obj['location']['city']
    db_obj.state = State.by_key(yelp_obj['location']['state_code'])
    db_obj.zip_code = yelp_obj['location']['postal_code']
    db_obj.latitude = float(yelp_obj['location']['coordinate']['latitude'])
    db_obj.longitude = float(yelp_obj['location']['coordinate']['longitude'])
    return db_obj


def text_to_object(text):
    name, address = parse_google_places(text)
    print name
    print address
    if name == None:
        return None
    search_results = yelp_api.search_query(term=name, location=address, sort=1)
    yelp_restaurant_object = search_results['businesses'][0]
    print yelp_restaurant_object
    yelp_id = yelp_restaurant_object['id']
    if Restaurant.objects.filter(yelp_id=yelp_id).exists():
        restaurant_object = Restaurant.objects.get(yelp_id=yelp_id)
    else:
        restaurant_object = Restaurant()
        restaurant_object = parse_yelp_obj(yelp_restaurant_object, restaurant_object)
        restaurant_object.save()
        for category in yelp_restaurant_object['categories']:
            category_obj, created = Category.objects.get_or_create(slug=category[1], name=category[0])
            if created:
                category_obj.save()
            restaurant_object.categories.add(category_obj)
    return restaurant_object
