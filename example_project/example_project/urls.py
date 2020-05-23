from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include, path

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', admin.site.urls),  # https://stackoverflow.com/a/43324478
]
