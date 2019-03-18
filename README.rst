=============================
django-stack-it
=============================

.. image:: https://badge.fury.io/py/django-stack-it.svg
    :target: https://badge.fury.io/py/django-stack-it

.. image:: https://travis-ci.org/Jufik/django_stack_it.svg?branch=master
    :target: https://travis-ci.org/Jufik/django_stack_it

.. image:: https://codecov.io/gh/jufik/django-stack-it/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jufik/django_stack_it

Content management system under development


Documentation
-------------

The full documentation is at https://django-stack-it.readthedocs.io.

Quickstart
----------

Install django-stack-it::

    pip install django-stack-it

Django Stack It relies on several dependencies, you need to add to your INSTALLED_APPS

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'polymorphic_tree',
        'polymorphic',
        'mptt',
        'imagekit',
        'stack_it'
        ...
    )
    
Add django-stack-it's URL patterns:

.. code-block:: python
    urlpatterns = [
        ...
        path(r'^', include('stack_it.urls')),
        ...
    ]
    
Basic Usage
----------
As soon as you a model is linked to a URL, it should inherit from the `Page` model.

.. code-block:: python
    from stack_it.models import Page

    class Article(Page):
        """
        Your model here
        """
        ....
Article is now considered to be a Page.
It comes with several usefull fields like `title`, `slug` dans `template_path`.

Register your model to the admin the way you want, 
and you can see all your website organization within one unified admin doing:

.. code-block:: python
    from stack_it.admin import PageAdmin as BasePageAdmin
    from stack_it.models import Page
    from blog.models import Article
    
    class PageAdmin(BasePageAdmin):
        base_model = Page
        child_models = (
            ...Your inherited model here,
            Article,
            ...
        )
     admin.site.register(Page, PageAdmin)

`Article` or any other model won't show up in the admin anymore.
Each model and model instances will be managed from the "Page" admin,
where all your pages are organized in a Drag n Drop interface to build up your site structure.

    
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
