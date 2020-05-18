.. Scrapy Django Dashboard documentation master file, created by sphinx-quickstart. You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.

Scrapy Django Dashboard - Documentation
=======================================

Scrapy Django Dashboard is a fork of `Django Dynamic Scraper (DDS) by Holger Drewes <https://github.com/holgerd77/django-dynamic-scraper>`_. It is a web app allowing users to create and manage Scrapy spiders through Django Admin dashboard.

.. note::
   Latest new features added :

   * Python ``3.7.7``
   * Django ``3.0.6``
   * Scrapy ``2.1.0`` 

   Due to the compatibility issues, the selected versions of celery, kombu and django-celery are placed in Root dir. Minor modifications in kombu package.
   
   * celery ``3.1``
   * modified kombu ``3.0.37``
   * django-celery ``3.3.1``

   * ``Javascript`` rendering
   * Scraping ``JSON`` content
   * More flexible ID and detail page URL(s) concept
   * Several checkers for a single scraper
   * Custom ``HTTP Header/Body``, ``Cookies``, ``GET/POST`` requests
   * ``Scrapy Meta`` attributes
   * Scraper/Checker ``Monitoring``

   See :ref:`releasenotes` for further details!

Features
--------

* Create and manage scrapers for your Django models in the Django admin interface
* Many features of Scrapy_ like regular expressions, processors, pipelines (see `Scrapy Docs`_)
* Image/screenshot scraping
* Dynamic scheduling depending on crawling success via Django Celery
* Checkers to check if items once scraped are still existing


.. _Scrapy: http://www.scrapy.org 
.. _`Scrapy Docs`: http://doc.scrapy.org


User Manual
-----------

.. toctree::
   :maxdepth: 2
   
   introduction
   installation
   getting_started
   advanced_topics
   basic_services
   reference
   development


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`