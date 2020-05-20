"""
Scrapy settings for `open_news` app

This conf file only contains most important settings by default. All the other settings are documented here:

http://doc.scrapy.org/topics/settings.html

"""

# Allows Python 2 to have the default interpretation of string literals be Unicode (UTF8)
from __future__ import unicode_literals
import os, sys

# `example_project` specifics
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../..")) 

# Download thumbnail issue
# [scrapy.pipelines.files] WARNING: File (code: 301): Error downloading file from <GET http://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/USA_orthographic.svg/100px-USA_orthographic.svg.png> referred in <None>
# Ref: https://stackoverflow.com/a/44137266
MEDIA_ALLOW_REDIRECTS = True

BOT_NAME = 'open_news'

#Setting LOG_STDOUT to True will prevent Celery scheduling to work, 2017-06-06
# Scrapy LOG_STDOUT defaults to False
# https://docs.scrapy.org/en/latest/topics/settings.html#log-stdout
# LOG_STDOUT = False 

LOG_LEVEL = 'INFO'

# A list of modules where Scrapy will look for spiders.
SPIDER_MODULES = [
    'scrapy_django_dashboard.spiders',
    'open_news.scraper',
]

# Use a very common UA
# USER_AGENT = '{b}/{v}'.format(b=BOT_NAME, v='1.0')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

# A dict containing the item pipelines to use, and their orders. 
# Order values are arbitrary, but it is customary to define them in the 0-1000 range. 
# Lower orders process before higher orders.
ITEM_PIPELINES = {
    'scrapy_django_dashboard.pipelines.DjangoImagesPipeline': 200,
    'scrapy_django_dashboard.pipelines.ValidationPipeline': 400,
    'open_news.scraper.pipelines.DjangoWriterPipeline': 800,
}

# Enabling your Media Pipeline
# Place 'scrapy_django_dashboard.pipelines.DjangoImagesPipeline' into `ITEM_PIPELINES`
# Configure the target storage setting to a valid value that will be used for storing the downloaded images. Otherwise the pipeline will remain disabled, even if you include it in the `ITEM_PIPELINES` setting.
IMAGES_STORE = os.path.join(PROJECT_ROOT, '../thumbnails')
# The Images Pipeline can automatically create thumbnails of the downloaded images.
IMAGES_THUMBS = {
    'medium': (50, 50),
    'small': (25, 25),
}

# More details here:
# https://scrapy-django-dashboard.readthedocs.io/en/latest/reference.html#reference
DSCRAPER_IMAGES_STORE_FORMAT = 'ALL'
DSCRAPER_LOG_ENABLED = True
DSCRAPER_LOG_LEVEL = 'ERROR'
DSCRAPER_LOG_LIMIT = 5