.. _installation:

Installation
============

.. _requirements:

Requirements
------------
The **prerequisites** for Scrapy Django Dashboard are as follows:

* Python_ 3.7.7
* Django_ 3.0.6
* Scrapy_ 2.1.0
* `scrapy-djangoitem`_ 1.1.1
* `Python JSONPath RW`_  1.4.0
* `Python-Future`_ 0.17.1 (Easy, clean, reliable Python 2/3 compatibility)

For **scheduling mechanism**, install `django-celery`_ ``3.3.1``:

Due to the compatibility issues, the selected versions of `celery`_ ``3.1``, `kombu`_ ``3.0.37`` and `django-celery`_ ``3.3.1`` reside in root dir. I have also made a quick fix in `kombu`_ ``3.0.37`` package to circumvent this well known issue. ::
    
    TypeError: __init__() missing 1 required positional argument: 'on_delete'

Find more about `Django ORM <on_delete> by reading the documentation`_.

For **scraping images**, install `Pillow`_ (PIL fork) ``5.4.1``:

For **javascript rendering**, install `Scrapy-Splash`_ ``0.7.2`` and :ref:`splash_optional`.
 
Installation
-------------------
Clone the source code with git ::

    git clone https://github.com/0xboz/scrapy_django_dashboard.git

**RECOMMENDATION**  

Run the code in a ``virtualenv``. For the sake of this docs, let us use `pyenv` to cheery-pick the local Python interpreter, create a virtual environment for the sample project, and finally install all required packages list in `requirements.txt`.

If you are running Debian OS, you are in luck. You can install `pyenv`_ with `a simple script`_. ::

    sudo apt install -y curl && curl https://raw.githubusercontent.com/0xboz/install_pyenv_on_debian/master/install.sh | bash

If you are planning to uninstall `pyenv` sometime in the future, run this command: ::

    curl https://raw.githubusercontent.com/0xboz/install_pyenv_on_debian/master/uninstall.sh | bash

Install Python and set it as the default interpreter locally. ::

    pyenv install 3.7.7
    pyenv local 3.7.7

Create a `virtualenv` with `pyenv-virtualenv`. ::

    pyenv virtualenv venv

Activate this `virtualenv`.::

    pyenv activate venv

Install all the required packages. ::

    (venv) pip install -r requirements.txt

In case you need to exit from this virtual environment. ::

    (venv) pyenv deactivate

Integration
-------------------

.. Note::
    The following steps will walk you through the setup of our `example_project`, which has been **ALREADY** included in the copy of GitHub clone. For your reference, check out `example_project` and find out more details. 

Start a new Django project. ::

    (venv) django-admin startproject example_project

This results in a `example_project` in the root dir with a structure like this: ::

    example_project/  
        example_project/
            __init__.py  
            settings.py  
            urls.py  
            wsgi.py  
        manage.py  

Now, let us move into `example_project` dir. ::

    (venv) cd example_project

Add ``scrapy_django_dashboard`` into ``INSTALLED_APPS`` in Django project settings. For more details, check out `example_project/settings.py`_.

Further, we create a demo app called `open_news`. ::

    (venv )python manage.py startapp open_news

.. _settingupscrapypython:

Scrapy
-----------------

.. _setting_up_scrapy:

Configuration
^^^^^^^^^^^^^^^^^^^^

For getting Scrapy_ to work the recommended way to start a new Scrapy project normally is to create a directory
and template file structure with the ``scrapy startproject myscrapyproject`` command on the shell first. 
However, there is (initially) not so much code to be written left and the directory structure
created by the ``startproject`` command cannot really be used when connecting Scrapy to the Django Dynamic Scraper
library. So the easiest way to start a new scrapy project is to just manually add the ``scrapy.cfg`` 
project configuration file as well as the Scrapy ``settings.py`` file and adjust these files to your needs.
It is recommended to just create the Scrapy project in the same Django app you used to create the models you
want to scrape and then place the modules needed for scrapy in a sub package called ``scraper`` or something
similar. After finishing this chapter you should end up with a directory structure similar to the following
(again illustrated using the open news example)::

  example_project/
    scrapy.cfg
    open_news/
      models.py # Your models.py file
      (tasks.py)      
      scraper/
        settings.py
        spiders.py
        (checkers.py)
        pipelines.py
      
Your ``scrapy.cfg`` file should look similar to the following, just having adjusted the reference to the
settings file and the project name::
  
  [settings]
  default = open_news.scraper.settings
  
  #Scrapy till 0.16
  [deploy]
  #url = http://localhost:6800/
  project = open_news

  #Scrapy with separate scrapyd (0.18+)
  [deploy:scrapyd1]
  url = http://localhost:6800/
  project = open_news 


And this is your ``settings.py`` file::

  import os
  
  PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings") #Changed in DDS v.0.3

  BOT_NAME = 'open_news'
  
  SPIDER_MODULES = ['dynamic_scraper.spiders', 'open_news.scraper',]
  USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')
  
  #Scrapy 0.20+
  ITEM_PIPELINES = {
      'dynamic_scraper.pipelines.ValidationPipeline': 400,
      'open_news.scraper.pipelines.DjangoWriterPipeline': 800,
  }

  #Scrapy up to 0.18
  ITEM_PIPELINES = [
      'dynamic_scraper.pipelines.ValidationPipeline',
      'open_news.scraper.pipelines.DjangoWriterPipeline',
  ]

The ``SPIDER_MODULES`` setting is referencing the basic spiders of DDS and our ``scraper`` package where
Scrapy will find the (yet to be written) spider module. For the ``ITEM_PIPELINES`` setting we have to
add (at least) two pipelines. The first one is the mandatory pipeline from DDS, doing stuff like checking
for the mandatory attributes we have defined in our scraper in the DB or preventing double entries already
existing in the DB (identified by the url attribute of your scraped items) to be saved a second time.  

.. _splash_optional:

Splash (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More and more webpages only show their full information load after various ``Ajax`` calls and/or ``Javascript`` 
function processing. For being able to scrape those websites ``DDS`` supports ``Splash`` for basic JS rendering/processing.

For this to work you have to install ``Splash`` (the Javascript rendering service) installed - probably via ``Docker``- 
(see `installation instructions <https://splash.readthedocs.org/en/latest/install.html>`_).

Tested versions to work with ``DDS``:
 
* Splash 1.8
* Splash 2.3  

Then ``scrapy-splash`` with::

    pip install scrapy-splash

Afterwards follow the configuration instructions on the `scrapy-splash GitHub page <https://github.com/scrapy-plugins/scrapy-splash#configuration>`_.

For customization of ``Splash`` args ``DSCRAPER_SPLASH_ARGS`` setting can be used (see: :ref:`settings`).

``Splash`` can later be used via activating it for certain scrapers in the corresponding ``Django Admin`` form.

.. note::
   Resources needed for completely rendering a website on your scraping machine are vastly larger then for just
   requesting/working on the plain HTML text without further processing, so make use of ``Splash`` capability
   on when needed!

.. _Python: https://www.python.org/
.. _Scrapy: http://www.scrapy.org/
.. _Django: https://www.djangoproject.com/
.. _`scrapy-djangoitem`: https://github.com/scrapy-plugins/scrapy-djangoitem
.. _`Python JSONPath RW`:  https://github.com/kennknowles/python-jsonpath-rw
.. _`Python-Future`: http://python-future.org/
.. _`django-celery`: https://github.com/celery/django-celery
.. _`celery`: https://github.com/celery/celery
.. _`kombu`: https://github.com/celery/kombu
.. _`Pillow`: https://python-pillow.github.io/
.. _`Scrapy-Splash`: https://github.com/scrapy-plugins/scrapy-splash
.. _`pyenv`: https://github.com/pyenv/pyenv

.. _`Django ORM <on_delete> by reading the documentation`: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
.. _`a simple script`: https://github.com/0xboz/install_pyenv_on_debian
.. _`example_project/settings.py`:  https://github.com/0xboz/scrapy_django_dashboard/blob/master/example_project/example_project/settings.py