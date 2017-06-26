"""
WSGI configuration for Flask.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
# pylint: skip-file
from application import app as application  # noqa
