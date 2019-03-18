# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
from tests.jsonenv import env

DEBUG = True
USE_TZ = True
USE_I18N = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "lf=g&ei5pq)3)1c9p*1e@_pl-2y64+rcc44+rv-02zc)6=ichc"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.get('db_name', ''),
        'USER': env.get('db_user', ''),
        'HOST': env.get('db_host', ''),
        'PASSWORD': env.get('db_password', ''),
        'PORT': '5432',
    }
}



ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.admin",
    "polymorphic_tree",
    "polymorphic",
    "mptt",
    "factory_generator",
    "imagekit",
    "tests",
    "stack_it",
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

FACTORY_NORMALIZE_FIELD_MAP = {
    'TreeForeignKey': 'ForeignKey',
    'PolymorphicTreeForeignKey': 'ForeignKey',
    'TranslationSlugField': 'SlugField',
    'TranslationBooleanField': 'BooleanField',
    'TranslationCharField': 'CharField'
}


def gettext(x): return x


LANGUAGES = (
    ('en-us', gettext('English (US)')),
    ('fr', gettext('French'))
)
LANGUAGE_CODE = 'en-us'
MODELTRANSLATION_AUTO_POPULATE = True
MODELTRANSLATION_ENABLE_FALLBACKS = True
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


FOLDER = 'folder'
BASE_FOLDER = FOLDER
MEDIA_FOLDERS = [
    'FOLDER',
]
MEDIA_FOLDER_CHOICES = tuple((globals()[i], globals()[i]) for i in MEDIA_FOLDERS)
