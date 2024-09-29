#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import environ


env = environ.Env()

DEBUG = os.environ.get("DEBUG")

switch_prod_dev = {"True": "dev", "False": "prod"}


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"core.config.{switch_prod_dev[str(DEBUG)]}_settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
