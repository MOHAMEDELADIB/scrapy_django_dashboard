============
Introduction
============

``Scrapy Django Dashboard`` allows you to create and manage `Scrapy`_ spiders through the Django Admin dashboard and save the scraped items into the database defined in Django models. 

``Scrapy Django Dashboard`` is well suited for some common scraping tasks, such as extracting a list of items (e.g. news and events) from the main page, and further fetching more information of each item from the detail page.

Here are some examples of using ``Scrapy Django Dashboard``:

* Local music events in a city
* New organic recipes for Asian foodies
* The latest articles from fashion blogs in NYC

``Scrapy Django Dashboard`` keeps the data structure separated from app models as much as possible. Therefore, it comes with its own Django model classes for the spiders, their runtime information and model attributes. Apart from a few foreign key relations, the app models can stay relatively independent.

``Scrapy Django Dashboard`` `GitHub`_ page contains a sample project in ``example_project`` directory. More details on this sample project are in :ref:`getting_started` guide.

.. _`Scrapy`: http://www.scrapy.org/
.. _`GitHub`: https://github.com/0xboz/scrapy_django_dashboard