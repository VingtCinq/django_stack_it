=============================
django_stack_it
=============================

.. image:: https://badge.fury.io/py/django_stack_it.svg
    :target: https://badge.fury.io/py/django_stack_it

.. image:: https://travis-ci.org/jufik/django_stack_it.svg?branch=master
    :target: https://travis-ci.org/jufik/django_stack_it

.. image:: https://codecov.io/gh/jufik/django_stack_it/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jufik/django_stack_it

Content management system: Pages is a list of (ordered) block and relevant content. Though to allow inline i18n content management, with high performance usage.

Documentation
-------------

The full documentation is at https://django_stack_it.readthedocs.io.

Quickstart
----------

Install django_stack_it::

    pip install django_stack_it

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stack_it',
        ...
    )

Add django_stack_it's URL patterns:

.. code-block:: python

    from stack_it import urls as stack_it_urls


    urlpatterns = [
        ...
        url(r'^', include(stack_it_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
