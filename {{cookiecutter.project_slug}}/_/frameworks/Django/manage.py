#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Main entry point of your Django application"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    # pylint: disable=import-outside-toplevel
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
