========================================
Scrapy Django Dashboard - Documentation
========================================

Scrapy Django Dashboard is a fork of `Django Dynamic Scraper (DDS) by Holger Drewes`_. It is a web app allowing users to create and manage Scrapy spiders through Django Admin dashboard.

.. note::
   Latest new features added :

   * Python ``3.7.7``
   * Django ``3.0.6``
   * Scrapy ``2.1.0``
   * Django Grappelli (Grid-based Django admin dashboard extension) ``2.14.2``
   * Javascript rendering
   * Scraping ``JSON`` content
   * More flexible ID and detail page URL(s) concept
   * Custom ``HTTP Header/Body``, ``Cookies``, ``GET/POST`` requests
   * Scrapy Meta attributes
   * Scraper/Checker Monitoring

Features
--------

* Create and manage Scrapy_ spiders via Django admin dashboard
* Support Scrapy_ regular expressions, processors, and pipelines (see `Scrapy Docs`_)
* Support image/screenshot scraping
* Schedule spiders via ``django-celery``
* Check existing items 

.. _`Django Dynamic Scraper (DDS) by Holger Drewes`: https://github.com/holgerd77/django-dynamic-scraper
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