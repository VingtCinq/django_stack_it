=============================
django-stack-it
=============================

.. image:: https://api.codacy.com/project/badge/Grade/4c1f910320434a5fb2fb828ebfcbaf95
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/Jufik/django_stack_it?utm_source=github.com&utm_medium=referral&utm_content=VingtCinq/django_stack_it&utm_campaign=Badge_Grade_Dashboard

.. image:: https://badge.fury.io/py/django-stack-it.svg
    :target: https://badge.fury.io/py/django-stack-it

.. image:: https://api.codacy.com/project/badge/Coverage/a842b7f950cd465d91d6b06c7d56ce16    
    :target: https://www.codacy.com/app/Jufik/django_stack_it?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=VingtCinq/django_stack_it&amp;utm_campaign=Badge_Coverage

.. image:: https://travis-ci.org/VingtCinq/django_stack_it.svg?branch=master
    :target: https://travis-ci.org/VingtCinq/django_stack_it
    
Content management system under development


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

To avoid migration messup, we strongly recomend you to deport `Stack It` migrations to your project.
This will avoid any unexpected conflict between environements, due to language addition/deletion.
In your settings:

.. code-block:: python
    MIGRATION_MODULES = {
        "stack_it":"tests.migrations"
    }

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

If you want your model's to be registered as usual, add `show_in_index = True` in your admin class to allow 
    
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
