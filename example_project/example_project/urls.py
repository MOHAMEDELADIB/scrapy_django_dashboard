from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # https://stackoverflow.com/a/43324478
]
