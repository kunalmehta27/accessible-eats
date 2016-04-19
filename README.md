# Accessible Eats
Accessible Eats is a Django-based web application that provides accessible restaurant recommendations. 

# Version
0.0.1

# Tech
Accessible Eats uses a number of APIs and Open Source projects to work properly.

* [Django] - Python based web framework
* [Yelp API] - Interface with Yelp to add restaurant data
* [Twilio] - Sends and receives text messages
* [Tweepy] - Python based Twitter API
* [Google Maps Geolocation] - Service used for geolocation
* [Twitter Bootstrap] - frontend web design
* [jQuery] - self explanatory

# Installation
First, clone the repository onto your local drive. 
```sh
$ git clone
```
The best way to develop in Django is by using a virtual environment. We recommend using [virtualenv]. An issue with virtualenv may be that it conflicts with Anaconda, to solve this simply uninstall Anaconda. You can create the necessary virtual environment by running
```sh
$ virtualenv -p python2.7 /tmp/accessible_eats/
```
and then activate by running
```sh
$ . /tmp/accessible_eats/bin/activate
```
Once you have activated your virtualenvironment, move to where you have cloned the repository. Then run
```sh
$ cd accessible_eats
```
at which point `ls` should yield a directory which has the file `requirements.txt`. Run
```sh
$ pip install -r requirements.txt
```
to install all of the dependencies for this project. 

Now, we need to set up the development settings.  `cd` back out to where you cloned the original project and find a folder entitled `open_source_settings`. Inside this folder, you will find a file called `settings.py`. Move this file to the folder `accessible_eats/accessible_eats`, which should have files called `urls.py` and `wsgi.py`. 

Open this settings file. We will need to update a number of variables to utilize the Accessible Eats Platform. 

1. `GOOGLE_API_KEY`: Create a Google Developer project and enable the following APIS: Google Places, Google Maps Geocoding and Google Maps Javascript. Find your API key credentials, and fill in the corresponding variable in `settings.py`.
2. **YELP Credentials**: You will also need a Yelp API Key to utilize the platform so create an account and similarly paste in the values into `settings.py`. 

Please note that due to the privacy and cost of the text message (Twilio) and Twitter (Tweepy) features of the platform, contributors to this project will not be able to access these APIs and the features will not work in local development. If you have suggestions for either of these features, please contact the owner of the repository. 

Once you have filled in the correct API keys. You should be able to run
```sh
$ python manage.py migrate
```
which will set up a database and then 
```sh
$ python manage.py runserver
```
which will create a locally hosted server for development. The codebase works primarily through the Django syntax and through fairly simple javascript. Much should be self-explanatory, but please see [Django] for more information. 

# Todos
* UI/UX Improvements
* Modularization and cleanup of code
* HTML and CSS cleanup
* Development of mobile application

# License
MIT


   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [virtualenv]: <https://virtualenv.pypa.io/en/latest/installation.html>
   [Yelp API]: <https://github.com/gfairchild/yelpapi>
   [twilio]: <https://www.twilio.com/>
   [Django]: <https://www.djangoproject.com/>
   [Tweepy]: <http://tweepy.readthedocs.org/en/v3.5.0/>
   [Google Maps Geolocation]: <https://console.developers.google.com/apis/>

