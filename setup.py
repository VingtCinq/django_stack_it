#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from stack_it/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("stack_it", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django_stack_it',
    version=version,
    description="""Content management system: Pages is a list of (ordered) block and relevant content. Though to allow inline i18n content management, with high performance usage.""",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author='Julien Kieffer',
    author_email='julien@vingtcinq.io',
    url='https://github.com/jufik/django_stack_it',
    packages=[
        'stack_it',
    ],
    include_package_data=True,
    install_requires=['Django>=2.1',
                      'django-imagekit',
                      'pillow',
                      'django-model-utils',
                      'django-mptt',
                      'django-polymorphic',
                      'django-polymorphic-tree',
                      ],
    license="MIT",
    zip_safe=False,
    keywords='django_stack_it',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
)
