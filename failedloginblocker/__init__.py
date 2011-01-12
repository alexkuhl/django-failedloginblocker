"""
Module for monitoring failed logins and blocking access through override of
django.contrib.auth.authenticate()
"""

version = '1.0.0'

from django.contrib import auth
from failedloginblocker.decorators import monitor_login

auth.authenticate = monitor_login( auth.authenticate )
