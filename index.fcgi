#!../bin/python
import sys, os

# Switch to the directory of your project. (Optional.)
#os.chdir(os.path.dirname(__file__))

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from django.core.servers.fastcgi import runfastcgi

runfastcgi(method="threaded", daemonize="false")