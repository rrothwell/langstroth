# Settings file to support demonstrations on the UAT (user acceptance testing) machine.

# Django settings for langstroth project.
from os import path
from os import environ

# Pick up the default settings then override them in this file.
from .defaults import *  # NOQA

TEST_MODE = False

# Have the install_uat.sh script sed them to the real passwords.
DB_PASSWORD = "dummy_db_password"
NAGIOS_PASSWORD = "dummy_nagios_password"

DEFAULT_DATABASE_NAME = 'langstroth'
ALLOCATION_DATABASE_NAME = 'allocations'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
     # See: https://docs.djangoproject.com/en/1.6/intro/tutorial01/
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DEFAULT_DATABASE_NAME,  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'langstroth_user',  # over-rides what is in my.cnf [client]
        'PASSWORD': DB_PASSWORD,  # over-rides what is in my.cnf [client]
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
        'OPTIONS': {
            'read_default_file': '/private/etc/my.cnf',
            'init_command': 'SET storage_engine=INNODB',  # Disable after the tables are created.
        },
    },
     # See: https://docs.djangoproject.com/en/1.6/topics/db/multi-db/
    'allocations_db': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ALLOCATION_DATABASE_NAME,  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'langstroth_user',  # over-rides what is in my.cnf [client]
        'PASSWORD': DB_PASSWORD,  # over-rides what is in my.cnf [client]
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
        'OPTIONS': {
            'read_default_file': '/private/etc/my.cnf',
            'init_command': 'SET storage_engine=INNODB',  # Disable after the tables are created.
        },
    }
}
DATABASE_ROUTERS = ['nectar_allocations.router.AllocationsRouter']

# Password strings populated by an edited version of the install_uat.sh script.
NAGIOS_URL = "http://langstroth.doesntexist.com/static/avail.html"
NAGIOS_AUTH = ("nectar", NAGIOS_PASSWORD)  # set password via sudo htpasswd /usr/local/nectar/.htpasswd nectar
NAGIOS_AVAILABILITY_URL = NAGIOS_URL
NAGIOS_STATUS_URL = "http://langstroth.doesntexist.com/static/status.html"

# Monkey patch nagios for the UAT environment.
import nagios_uat

GRAPHITE_URL = "http://graphite.dev.rc.nectar.org.au"

# Additional locations of static files
STATICFILES_DIRS = (
    path.join(path.dirname(__file__), "static"),
    path.join(path.dirname(__file__), "data"),

    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'langstroth',
    'nectar_status',
    'nectar_allocations',
    'user_statistics',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
