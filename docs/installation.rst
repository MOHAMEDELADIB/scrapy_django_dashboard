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
------------
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

.. _splash_optional:

Splash (Optional)
-----------------

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