from django.conf.urls import include, url
from django.contrib import admin
from accessible_eats_app import urls as ae_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(ae_urls)),
]
