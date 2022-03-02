from setuptools import setup

import os

setup(
    name='scrapy-django-dashboard',
    version='1.0',
    description='Scrapy Spiders Over Django Admin Dashboard – A Fork From Django-Dynamic-Scraper',
    author='0xboz',
    author_email='0xboz@hacari.com',
    url='https://github.com/0xboz/scrapy_django_dashboard',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    license='MIT',
    platforms=['OS Independent'],
    packages=[
        'scrapy_django_dashboard',
        'scrapy_django_dashboard.management',
        'scrapy_django_dashboard.management.commands',
        'scrapy_django_dashboard.migrations',
        'scrapy_django_dashboard.south_migrations',
        'scrapy_django_dashboard.spiders',
        'scrapy_django_dashboard.utils',
    ],
    package_data = {
        'scrapy_django_dashboard': [
            'static/js/*',
        ],
    },
    install_requires=[
    #    Django, Scrapy and Celery requirements are commented out here and have
    #    to be installed manually to avoid side-effects when updating the software.
    #    Version numbers are updated accordingly though.
    #    'Django==3.0.6',
    #    'Scrapy==2.1.0',
    #    'scrapy-djangoitem==1.1.1',
    #    'scrapy-splash==0.7.2', # Optional
    #    'scrapyd==1.2.1',
        'jsonpath-rw==1.4.0',
    #    Use kombu/celery/django-celery in the root instead
    #    'kombu>=3.0.37,<3.1',
    #    'Celery==3.1.25',
    #    'django-celery==3.2.1', # Scheduling
        'future==0.17.1',
        'pillow==9.0.0',
        'attrs==19.3.0',
    ],
    classifiers=[
        'Development Status :: Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
