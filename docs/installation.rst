.. _installation:

============
Installation
============

.. _requirements:

Prerequisites
-------------

The **prerequisites** for ``Scrapy Django Dashboard`` are as follows:

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

.. _manual_installation:

Manual Installation
-------------------

Clone the source code with git ::

    git clone https://github.com/0xboz/scrapy_django_dashboard.git

.. Note::
    **RECOMMENDATION:**  Run the code in a ``virtualenv``. For the sake of this docs, let us use `pyenv` to cheery-pick the local Python interpreter, create a virtual environment for the sample project, and finally install all required packages list in `requirements.txt`.

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
^^^^^^^^^^^^^^^^^

``Scrapy Django Dashboard`` supports `Splash`_ (A javascript rendering service).

Install `Splash`_ (see `Splash Installation Instructions`_).

Tested versions:
 
* Splash ``1.8``
* Splash ``2.3`` 

Once `Splash`_ is up running, install `Scrapy-Splash`_ ::

    (venv) pip install scrapy-splash

Refer to `Scrapy-Splash GitHub configuration page`_ for further instructions.

To customize ``Splash`` args, use ``DSCRAPER_SPLASH_ARGS`` (see: :ref:`settings`). 

``Splash`` can be later activated in `Django` Admin dashboard.

.. note::
   Resources needed for completely rendering a website on your scraping machine are vastly larger then for just requesting/working on the plain HTML text without further processing, so make use of ``Splash`` capability on when needed!

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

.. _`Splash`: https://github.com/scrapinghub/splash
.. _`Splash Installation Instructions`: https://splash.readthedocs.io/en/latest/install.html
.. _`Scrapy-Splash GitHub configuration page`: https://github.com/scrapy-plugins/scrapy-splash#configuration