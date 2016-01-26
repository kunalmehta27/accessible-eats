from yelpapi import YelpAPI
import urllib, urllib2
import json


GOOGLE_API_KEY = 'AIzaSyDnAkO8M2ykT71YBC0WmSfmZtEUhnoCN50'
yelp_api = YelpAPI('US2mtMpskJ36JSb_n6Uy-w', 'gtu09XfGR3FwC_Ar7LLYGEB-3EM', 'fIvJ3B48nF_Ro6QP5C-m6ptJOQHB5p7u', '8lApWweZlez8vmlBYQ5mNMW3pWI')

def parse_google_places(name):
	name = urllib.quote(name)
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' % (name, GOOGLE_API_KEY)
	page = urllib2.urlopen(url)
	data = page.read()
	obj = json.loads(data)
	name = obj['results'][0]['name']
	address = obj['results'][0]['formatted_address']
	return name, address

name = "Leals 79124"
name, address = parse_google_places(name)
search_results = yelp_api.search_query(term = name, location=address)
yelp_restaurant_object = search_results['businesses'][0]

