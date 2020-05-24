.. _getting_started:

===============
Getting Started
===============

In this tutorial, we are going to use ``example_project`` and its ``open_news`` app to walk you through how to integrate ``Scrapy Django Dashboard`` into a typical Django project.

The tutorial itself can be roughly divided into two parts: 

  * :ref:`part_one`: Set up example project, open news app and a Scrapy spider.

  * :ref:`part_two`: Create parameters in Django admin dashboard accordingly.

.. Note::
    GitHub_ has **ALREADY** included the source code of this sample project.

.. _GitHub: https://github.com/0xboz/scrapy_django_dashboard

.. _project_summary:

Project Summary
---------------

The code scrapes the news URLs, thumbnails and excerpts from the main page of WikiNews_. Further, it collects the news title from each news detail page. This might sound redundant at first, but it is a selected way to demonstrate the difference in ``Main Page (MP)`` and ``Detail Page (DP)`` as we deploy the spiders in a real project. 

.. _Wikinews: http://en.wikinews.org/wiki/Main_Page

.. Note::

  The following instructions assume you have already finished the :ref:`installation` successfully. ``(venv)`` means a virtual environment is activated in advance, which is considered as the best practice when running the code without the potential breaking OS global packages.

.. _part_one:

PART ONE
--------

In Part One, we will mainly use prompt commands and a text editor to generate a minimal amount of boilerplate and other setting files manually. 


.. _creating_example_project:

Creating Example Project 
^^^^^^^^^^^^^^^^^^^^^^^^

Run this command: ::

    (venv) django-admin startproject example_project

.. note::

  This might not be the best practice when starting a new Django project, according to The `Hitchhikers' Guide to Python`_, which suggests the following command instead to avoid repetitive paths by appending ``.`` at the end. ::

    (venv) django-admin startproject example_project . 

  However, this tutorial sticks with `the official Django Tutorial Part 1`_ for the sake of consistency.

.. _`Hitchhikers' Guide to Python`: https://docs.python-guide.org/writing/structure/#regarding-django-applications

.. _`the official Django Tutorial Part 1`: https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project

This results in a ``example_project/`` in the root directory with a directory tree like this: ::

    example_project/  
        example_project/
            __init__.py  
            settings.py  
            urls.py  
            wsgi.py  
        manage.py  

Now, let us navigate into ``example_project/``. ::

    (venv) cd example_project

Add ``scrapy_django_dashboard`` into ``INSTALLED_APPS`` in ``settings.py``. For more detailed comments, check out `example_project/example_project/settings.py`_ on `GitHub`_.  

.. _`example_project/example_project/settings.py`:  https://github.com/0xboz/scrapy_django_dashboard/blob/master/example_project/example_project/settings.py


.. _creating_open_news_app:

Creating Open News App
^^^^^^^^^^^^^^^^^^^^^^

Next, we create ``open_news`` app by running this command in ``example_project/example_project/`` (where ``manage.py`` resides). ::

    (venv) python manage.py startapp open_news

This results in a ``open_news/`` with a directory tree like this: ::

    open_news/  
        migrations/
            __init__.py
        __init__.py  
        admin.py
        apps.py
        models.py
        tests.py
        views.py


.. _creating_open_news_app_models:

Creating Open News App Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``open_news`` app, we need to create at least *two model classes*. The first class stores the scraped data (``Articles`` in our example), and the second one (``NewsWebsite`` in our example) acts as a reference model class defining the ``origin/category/topic`` where the scraped items belong to. 

Here is our ``model.py``. ::

  # example_project/example_project/open_news/model.py

  from __future__ import unicode_literals
  from django.db import models
  from django.db.models.signals import pre_delete
  from django.dispatch import receiver
  from scrapy_djangoitem import DjangoItem
  from scrapy_django_dashboard.models import Scraper, SchedulerRuntime
  from six import python_2_unicode_compatible


  @python_2_unicode_compatible
  class NewsWebsite(models.Model):
      name = models.CharField(max_length=200)
      url = models.URLField()
      scraper = models.ForeignKey(
          Scraper, blank=True, null=True, on_delete=models.SET_NULL)
      scraper_runtime = models.ForeignKey(
          SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

      def __str__(self):
          return self.name


  @python_2_unicode_compatible
  class Article(models.Model):
      title = models.CharField(max_length=200)
      news_website = models.ForeignKey(
          NewsWebsite, blank=True, null=True, on_delete=models.SET_NULL)
      description = models.TextField(blank=True)
      url = models.URLField(blank=True)
      thumbnail = models.CharField(max_length=200, blank=True)
      checker_runtime = models.ForeignKey(
          SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

      def __str__(self):
          return self.title


  class ArticleItem(DjangoItem):
      django_model = Article


  @receiver(pre_delete)
  def pre_delete_handler(sender, instance, using, **kwargs):
      if isinstance(instance, NewsWebsite):
          if instance.scraper_runtime:
              instance.scraper_runtime.delete()

      if isinstance(instance, Article):
          if instance.checker_runtime:
              instance.checker_runtime.delete()


  pre_delete.connect(pre_delete_handler)

We have defined some foreign key fields referencing ``Scrapy Django Dashboard`` models. The ``NewsWebsite`` class refers to the :ref:`scraper` model, which contains the main scraper with information about how to scrape the attributes of the article objects. The ``scraper_runtime`` field is a reference to the :ref:`scheduler_runtime` class from ``Scrapy Django Dashboard`` models. This object stores the scraper schedules. 

The ``NewsWebsite`` class also has to provide the url to be used during the scraping process. You can either use (if existing) the representative url field of the model class, which is pointing to the nicely-layouted overview news page also visited by the user. In this case we are choosing this way with taking the ``url`` attribute of the model class as the scrape url. However, it often makes sense to provide a dedicated ``scrape_url`` (you can name the attribute freely) field for cases, when the representative url differs from the scrape url (e.g. if list content is loaded via ajax, or if you want to use another format of the content - e.g. the rss feed - for scraping).

The ``Article`` model class has a class attribute called ``checker_runtime``, a reference to :ref:`scheduler_runtime` ``Scrapy Django Dashboard`` model class. This scheduling object holds information about the next check and evaluates if the news article still exists or it can be deleted (see :ref:`item_checkers`) by using the ``url`` of ``Article``.

Last but not least, ``Scrapy Django Dashboard`` uses the DjangoItem_ class from Scrapy to store the scraped data into the database.

.. _DjangoItem: https://scrapy.readthedocs.org/en/latest/topics/djangoitem.html

.. note::

   To have a loose coupling between the runtime objects and the domain model objects, we declare the foreign keys to the ``Scrapy Django Dashboard`` objects with ``blank=True, null=True, on_delete=models.SET_NULL``. This prevents the reference object and the associated scraped objects from being deleted when we remove a ``Scrapy Django Dashboard`` object by accident.

.. note::

  When we delete model objects via the Django admin dashboard, the runtime objects are not removed. To enable this feature,use `Django's pre_delete signals`_ in your ``models.py`` to delete e.g. the ``checker_runtime`` when deleting an article ::

    @receiver(pre_delete)
    def pre_delete_handler(sender, instance, using, **kwargs):
        ....
        
        if isinstance(instance, Article):
            if instance.checker_runtime:
                instance.checker_runtime.delete()
                
    pre_delete.connect(pre_delete_handler)

.. _`Django's pre_delete signals`: https://docs.djangoproject.com/en/dev/topics/db/models/#overriding-model-methods


.. _configuring_scrapy:

Configuring Scrapy
^^^^^^^^^^^^^^^^^^

The common way to start a Scrapy project with boilerplate files is to run: ::

  scrapy startproject my_scrapy_project

However, this approach does not save much time down the road, because the boilerplate code can not directly interact with ``Scrapy Django Dashboard`` app without manual configuration.

Therefore, **the preferred way** is to create ``scrapy.cfg`` file in ``example_project/`` manually (where ``open_news/`` resides). Further, create ``scrapy/`` in ``open_news/``, and add the following files according to this following directory tree. ::

    example_project/  
        example_project/
            __init__.py  
            settings.py  
            urls.py  
            wsgi.py 
        open_news/  
            migrations/
                __init__.py
            scraper/  # Manually added
                __init__.py  # Manually added
                checkers.py  # Manually added
                pipelines.py  # Manually added
                settings.py  # Manually added
                spiders.py  # Manually added
            __init__.py  
            admin.py
            apps.py
            models.py
            tasks.py  # Manually added
            tests.py
            views.py         
        manage.py
        scrapy.cfg  # Manually added
        
.. note::

  It is recommended to create a Scrapy project within the app of interest. To achieve this, create the necessary modules for the Scrapy project in a sub directory (``scraper`` in our example) of this app. 

Here is what ``scrapy.cfg`` looks like: (Make proper changes, such as app name in your own project.) ::
 
  # example_project/example_project/scrapy.cfg

  # Define open_news app scrapy settings
  [settings]
  default = open_news.scraper.settings

  # Scrapy deployment using scrapyd
  [deploy:scrapyd1]
  url = http://localhost:6800/
  project = open_news

And here is ``settings.py`` in ``example_project/example_project/open_news/scraper/``. ::

  # example_project/example_project/open_news/scraper/settings.py

  from __future__ import unicode_literals
  import os
  import sys

  PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")
  sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../.."))

  MEDIA_ALLOW_REDIRECTS = True

  BOT_NAME = 'open_news'

  LOG_LEVEL = 'DEBUG'

  SPIDER_MODULES = [
      'scrapy_django_dashboard.spiders',
      'open_news.scraper',
  ]

  USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

  ITEM_PIPELINES = {
      'scrapy_django_dashboard.pipelines.DjangoImagesPipeline': 200,
      'scrapy_django_dashboard.pipelines.ValidationPipeline': 400,
      'open_news.scraper.pipelines.DjangoWriterPipeline': 800,
  }

  IMAGES_THUMBS = {
      'medium': (50, 50),
      'small': (25, 25),
  }

  DSCRAPER_IMAGES_STORE_FORMAT = 'ALL'
  DSCRAPER_LOG_ENABLED = True
  DSCRAPER_LOG_LEVEL = 'ERROR'
  DSCRAPER_LOG_LIMIT = 5

The ``SPIDER_MODULES`` is a list of the spider modules of ``Scrapy Django Dashboard`` app and ``scraper`` package where Scrapy will look for spiders. In ``ITEM_PIPELINES``, ``scrapy_django_dashboard.pipelines.DjangoImagesPipeline``, a sub-class of ``scrapy.pipelines.images.ImagesPipeline``, enables scraping image media files; ``scrapy_django_dashboard.pipelines.ValidationPipeline`` checks the mandatory attributes and prevents duplicate entries by examining the unique key (the url attribute in our example). 

.. note::

  Refer to `GitHub`_ for more detailed comments in ``open_news/scraper/settings.py``.

To make Scrapy interact with Django objects, we need two more static classes: one being a spider class, a sub-class of :ref:`django_spider`,  and the other being a Scrapy pipeline to save scraped items.

.. _creating_scrapy_spider:

Creating Scrapy Spider
""""""""""""""""""""""

Our ``ArticleSpider``, a sub-class of :ref:`django_spider`, references itself to the domain model class ``NewsWebsite``. ::

  # example_project/example_project/open_news/scraper/spiders.py

  from __future__ import unicode_literals
  from scrapy_django_dashboard.spiders.django_spider import DjangoSpider
  from open_news.models import NewsWebsite, Article, ArticleItem


  class ArticleSpider(DjangoSpider):

      name = 'article_spider'

      def __init__(self, *args, **kwargs):
          self._set_ref_object(NewsWebsite, **kwargs)
          self.scraper = self.ref_object.scraper
          self.scrape_url = self.ref_object.url
          self.scheduler_runtime = self.ref_object.scraper_runtime
          self.scraped_obj_class = Article
          self.scraped_obj_item_class = ArticleItem
          super(ArticleSpider, self).__init__(self, *args, **kwargs)


.. _creating_scrapy_pipeline:

Creating Scrapy Pipeline
""""""""""""""""""""""""

``Scrapy Django Dashboard`` allows additional attributes to be added to the scraped items by requiring custom item pipelines. ::

  # example_project/open_news/scraper/pipelines.py

  from __future__ import unicode_literals
  from builtins import str
  from builtins import object
  import logging
  from django.db.utils import IntegrityError
  from scrapy.exceptions import DropItem
  from scrapy_django_dashboard.models import SchedulerRuntime


  class DjangoWriterPipeline(object):

      def process_item(self, item, spider):
          if spider.conf['DO_ACTION']:
              try:
                  item['news_website'] = spider.ref_object

                  checker_rt = SchedulerRuntime(runtime_type='C')
                  checker_rt.save()
                  item['checker_runtime'] = checker_rt

                  item.save()
                  spider.action_successful = True
                  spider.logger.info("{cs}Item {id} saved to Django DB.{ce}".format(
                      id=item._id_str,
                      cs=spider.bcolors['OK'],
                      ce=spider.bcolors['ENDC']))

              except IntegrityError as e:
                  spider.logger.error(str(e))
                  raise DropItem("Missing attribute.")

          return item


**TODO**

The things you always have to do here is adding the reference object to the scraped item class and - if you
are using checker functionality - create the runtime object for the checker. You also have to set the
``action_successful`` attribute of the spider, which is used internally when the spider is closed.


.. _database_migration_authorization:

Database Migration & Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, we head back to ``example_project/`` (where ``manage.py`` resides). When dealing a custom app (``open_news`` in our example), we need to make database migrations: ::

  (venv) python manage.py makemigrations open_news

This creates a SQLite database file in ``example_project/example_project/``, called ``example_project.db``. Feel free to change db location by changing ``example_project/example_project/settings.py`` as needed. Now, we can migrate the database. ::

  (venv) python migrate

This creates a SQLite database file in ``example_project.db`` in ``example_project/example_project/``. Feel free to change db location by tweaking ``example_project/example_project/settings.py`` as needed.

We also need an account to log into Django admin dashboard. ::

  (venv) python manage.py createsuperuser

Fill out username, email and password. Next, power up the development server and load Django admin page. ::

  (venv) python manage.py runserver

The default admin page should be ``http://localhost:8000/admin``.


.. _part_two:

PART TWO
--------

In Part Two, our configurations take place primarily in Django admin dashboard, prior to starting the spider from the prompt.


.. _defining_item_object_class:

Defining Item Object Class
--------------------------

Now, log into Django admin dashboard, it should look similar to this:

.. image:: images/screenshot_django_admin_overview.png

Before being able to create scrapers in Django Dynamic Scraper you have to define which parts of the Django
model class you defined above should be filled by your scraper. This is done via creating a new 
:ref:`scraped_obj_class` in your Django admin interface and then adding several :ref:`scraped_obj_attr` 
datasets to it, which is done inline in the form for the :ref:`scraped_obj_class`. All attributes for the
object class which are marked as to be saved to the database have to be named like the attributes in your 
model class to be scraped. In our open news example
we want the title, the description, and the url of an Article to be scraped, so we add these attributes with
the corresponding names to the scraped obj class.

The reason why we are redefining these attributes here, is that we can later define x_path elements for each
of theses attributes dynamically in the scrapers we want to create. When Django Dynamic Scraper
is scraping items, the **general workflow of the scraping process** is as follows:

* The DDS scraper is scraping base elements from the overview page of items beeing scraped, with each base
  element encapsulating an item summary, e.g. in our open news example an article summary containing the
  title of the article, a screenshot and a short description. The encapsuling html tag often is a ``div``,
  but could also be a ``td`` tag or something else.
* If provided the DDS scraper is then scraping the url from this item summary block leading to a detail page of the
  item providing more information to scrape
* All the real item attributes (like a title, a description, a date or an image) are then scraped either from 
  within the item summary block on the overview page or from a detail page of the item. This can be defined later
  when creating the scraper itself.

To define which of the scraped obj attributes are just simple standard attributes to be scraped, which one
is the base attribute (this is a bit of an artificial construct) and which one eventually is a url to be followed
later, we have to choose an attribute type for each attribute defined. There is a choice between the following
types (taken from ``dynamic_scraper.models.ScrapedObjAttr``)::

  ATTR_TYPE_CHOICES = (
      ('S', 'STANDARD'),
      ('T', 'STANDARD (UPDATE)'),
      ('B', 'BASE'),
      ('U', 'DETAIL_PAGE_URL'),
      ('I', 'IMAGE'),
  )

``STANDARD``, ``BASE`` and ``DETAIL_PAGE_URL`` should be clear by now, ``STANDARD (UPDATE)`` behaves like ``STANDARD``, 
but these attributes are updated with the new values if the item is already in the DB. ``IMAGE`` represents attributes which will 
hold images or screenshots. So for our open news example we define a base attribute called 'base' with 
type ``BASE``, two standard elements 'title' and 'description' with type ``STANDARD`` 
and a url field called 'url' with type ``DETAIL_PAGE_URL``. Your definition form for your scraped obj class 
should look similar to the screenshot below:

.. image:: images/screenshot_django-admin_add_scraped_obj_class.png

To prevent double entries in the DB you also have to set one or more object attributes of type ``STANDARD`` or 
``DETAIL_PAGE_URL`` as ``ID Fields``. If you provide a ``DETAIL_PAGE_URL`` for your object scraping, it is often a
good idea to use this also as an ``ID Field``, since the different URLs for different objects should be unique by
definition in most cases. Using a single ``DETAIL_PAGE_URL`` ID field is also prerequisite if you want to use the
checker functionality (see: :ref:`item_checkers`) of DDS for dynamically detecting and deleting items not existing
any more.

Also note that these ``ID Fields`` just provide unique identification of an object for within the scraping process. In your
model class defined in the chapter above you can use other ID fields or simply use a classic numerical auto-incremented
ID provided by your database.

.. note::
   If you define an attribute as ``STANDARD (UPDATE)`` attribute and your scraper reads the value for this attribute from the detail page
   of the item, your scraping process requires **much more page requests**, because the scraper has to look at all the detail pages
   even for items already in the DB to compare the values. If you don't use the update functionality, use the simple ``STANDARD``
   attribute instead!

.. note::
   The ``order`` attribute for the different object attributes is just for convenience and determines the
   order of the attributes when used for defining ``XPaths`` in your scrapers. Use 10-based or 100-based steps
   for easier resorting (e.g. '100', '200', '300', ...).


Defining your scrapers
======================

General structure of a scraper
------------------------------

Scrapers for Django Dynamic Scraper are also defined in the Django admin interface. You first have to give the
scraper a name and select the associated :ref:`scraped_obj_class`. In our open news example we call the scraper
'Wikinews Scraper' and select the :ref:`scraped_obj_class` named 'Article' defined above.

The main part of defining a scraper in DDS is to create several scraper elements, each connected to a 
:ref:`scraped_obj_attr` from the selected :ref:`scraped_obj_class`. Each scraper element define how to extract 
the data for the specific :ref:`scraped_obj_attr` by following the main concepts of Scrapy_ for scraping
data from websites. In the fields named 'x_path' and 'reg_exp' an XPath and (optionally) a regular expression
is defined to extract the data from the page, following Scrapy's concept of 
`XPathSelectors <http://readthedocs.org/docs/scrapy/en/latest/topics/selectors.html>`_. The 'request_page_type'
select box tells the scraper if the data for the object attibute for the scraper element should be extracted
from the overview page or a detail page of the specific item. For every chosen page type here you have to define a
corresponding request page type in the admin form above. The fields 'processors' and 'processors_ctxt' are
used to define output processors for your scraped data like they are defined in Scrapy's
`Item Loader section <http://readthedocs.org/docs/scrapy/en/latest/topics/loaders.html>`_.
You can use these processors e.g. to add a string to your scraped data or to bring a scraped date in a
common format. More on this later. Finally, the 'mandatory' check box is indicating whether the data
scraped by the scraper element is a necessary field. If you define a scraper element as necessary and no
data could be scraped for this element the item will be dropped. You always have to keep attributes
mandatory if the corresponding attributes of your domain model class are mandatory fields, otherwise the 
scraped item can't be saved in the DB.

For the moment, keep the ``status`` to ``MANUAL`` to run the spider via the command line during this tutorial.
Later you will change it to ``ACTIVE``. 

Creating the scraper of our open news example
---------------------------------------------

Let's use the information above in the context of our Wikinews_ example. Below you see a screenshot of an
html code extract from the Wikinews_ overview page like it is displayed by the developer tools in Google's 
Chrome browser:
 
.. image:: images/screenshot_wikinews_overview_page_source.png

The next screenshot is from a news article detail page:

.. image:: images/screenshot_wikinews_detail_page_source.png

We will use these code snippets in our examples.

.. note::
  If you don't want to manually create the necessary DB objects for the example project, you can also run
  ``python manage.py loaddata open_news/open_news_dds_[DDS_VERSION].json`` from within the ``example_project`` 
  directory in your favorite shell to have all the objects necessary for the example created automatically.
  Use the file closest to the current DDS version. If you run into problems start installing the fitting
  DDS version for the fixture, then update the DDS version and apply the latest Django migrations.
  
.. note::
   The WikiNews site changes its code from time to time. I will try to update the example code and text in the
   docs, but I won't keep pace with the screenshots so they can differ slightly compared to the real world example.

1. First we have to define a base 
scraper element to get the enclosing DOM elements for news item
summaries. On the Wikinews_ overview page all news summaries are enclosed by ``<td>`` tags with a class
called 'l_box', so ``//td[@class="l_box"]`` should do the trick. We leave the rest of the field for the 
scraper element on default.

2. It is not necessary but just for the purpose of this example let's scrape the title of a news article
from the article detail page. On an article detail page the headline of the article is enclosed by a
``<h1>`` tag with an id named 'firstHeading'. So ``//h1[@id="firstHeading"]/text()`` should give us the headline.
Since we want to scrape from the detail page, we have to activate the 'from_detail_page' check box.

3. All the standard elements we want to scrape from the overview page are defined relative to the
base element. Therefore keep in mind to leave the trailing double slashes of XPath definitions.
We scrape the short description of a news item from within a ``<span>`` tag with a class named 'l_summary'.
So the XPath is ``p/span[@class="l_summary"]/text()``.

4. And finally the url can be scraped via the XPath ``span[@class="l_title"]/a/@href``. Since we only scrape 
the path of our url with this XPath and not the domain, we have to use a processor for the first time to complete
the url. For this purpose there is a predefined processor called 'pre_url'. You can find more predefined
processors in the ``dynamic_scraper.utils.processors`` module - see :ref:`processors` for processor reference - 'pre_url' is simply doing what we want,
namely adding a base url string to the scraped string. To use a processor, just write the function name
in the processor field. Processors can be given some extra information via the processors_ctxt field.
In our case we need the spefic base url our scraped string should be appended to. Processor context
information is provided in a dictionary like form: ``'processor_name': 'context'``, in our case:
``'pre_url': 'http://en.wikinews.org'``. Together with our scraped string this will create
the complete url.

.. image:: images/screenshot_django-admin_scraper_1.png
.. image:: images/screenshot_django-admin_scraper_2.png

This completes the xpath definitions for our scraper. The form you have filled out should look similar to the screenshot above 
(which is broken down to two rows due to space issues).

.. note::
   You can also **scrape** attributes of your object **from outside the base element** by using the ``..`` notation
   in your XPath expressions to get to the parent nodes!

.. note::
   Starting with ``DDS v.0.8.11`` you can build your **detail page URLs** with
   placeholders for **main page attributes** in the form of ``{ATTRIBUTE_NAME}``, see :ref:`attribute_placeholders` for further reference.


.. _adding_request_page_types:

Adding corresponding request page types
---------------------------------------

For all page types you used for your ``ScraperElemes`` you have to define corresponding ``RequestPageType`` objects
in the ``Scraper`` admin form. There has to be exactly one main page and 0-25 detail page type objects.

.. image:: images/screenshot_django-admin_request_page_type_example.png

Within the ``RequestPageType`` object you can define request settings like the content type (``HTML``, ``XML``,...),
the request method (``GET`` or ``POST``) and others for the specific page type. With this it is e.g. possible to 
scrape HTML content from all the main pages and ``JSON`` content from the followed detail pages. For more information
on this have a look at the :ref:`advanced_request_options` section.

Create the domain entity reference object (NewsWebsite) for our open news example
---------------------------------------------------------------------------------

Now - finally - we are just one step away of having all objects created in our Django admin.
The last dataset we have to add is the reference object of our domain, meaning a ``NewsWebsite``
object for the Wikinews Website.

To do this open the NewsWebsite form in the Django admin, give the object a meaningful name ('Wikinews'),
assign the scraper and create an empty :ref:`scheduler_runtime` object with ``SCRAPER`` as your
``runtime_type``. 

.. image:: images/screenshot_django-admin_add_domain_ref_object.png

.. _running_scrapers:

Running/Testing your scraper
============================

You can run/test spiders created with Django Dynamic Scraper from the command line similar to how you would run your
normal Scrapy spiders, but with some additional arguments given. The syntax of the DDS spider run command is
as following::

  scrapy crawl [--output=FILE --output-format=FORMAT] SPIDERNAME -a id=REF_OBJECT_ID 
                          [-a do_action=(yes|no) -a run_type=(TASK|SHELL) 
                          -a max_items_read={Int} -a max_items_save={Int}
                          -a max_pages_read={Int}
                          -a start_page=PAGE -a end_page=PAGE
                          -a output_num_mp_response_bodies={Int} -a output_num_dp_response_bodies={Int} ]
  
* With ``-a id=REF_OBJECT_ID`` you provide the ID of the reference object items should be scraped for,
  in our example case that would be the Wikinews ``NewsWebsite`` object, probably with ID 1 if you haven't
  added other objects before. This argument is mandatory.
  
* By default, items scraped from the command line are not saved in the DB. If you want this to happen,
  you have to provide ``-a do_action=yes``.
  
* With ``-a run_type=(TASK|SHELL)`` you can simulate task based scraper runs invoked from the 
  command line. This can be useful for testing, just leave this argument for now.

* With ``-a max_items_read={Int}`` and ``-a max_items_save={Int}`` you can override the scraper settings for these
  params.

* With ``-a max_pages_read={Int}`` you can limit the number of pages read when using pagination

* With ``-a start_page=PAGE`` and/or ``-a end_page=PAGE`` it is possible to set a start and/or end page

* With ``-a output_num_mp_response_bodies={Int}`` and ``-a output_num_dp_response_bodies={Int}`` you can log
  the complete response body content of the {Int} first main/detail page responses to the screen for debugging
  (beginnings/endings are marked with a unique string in the form ``RP_MP_{num}_START`` for using full-text
  search for orientation)

* If you don't want your output saved to the Django DB but to a custom file you can use Scrapy's build-in 
  output options ``--output=FILE`` and ``--output-format=FORMAT`` to scrape items into a file. Use this without 
  setting the ``-a do_action=yes`` parameter! 

So, to invoke our Wikinews scraper, we have the following command::

  scrapy crawl article_spider -a id=1 -a do_action=yes
  

If you have done everything correctly (which would be a bit unlikely for the first run after so many single steps,
but just in theory... :-)), you should get some output similar to the following, of course with other 
headlines: 

.. image:: images/screenshot_scrapy_run_command_line.png

In your Django admin interface you should now see the scraped articles listed on the article overview page:

.. image:: images/screenshot_django-admin_articles_after_scraping.png

Phew.

Your first scraper with Django Dynamic Scraper is working. Not so bad! If you do a second run and there
haven't been any new bugs added to the DDS source code in the meantime, no extra article objects should be added
to the DB. If you try again later when some news articles changed on the Wikinews overview page, the new
articles should be added to the DB. 






