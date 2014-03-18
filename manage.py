#!/usr/bin/env python
import dotenv
import os
import sys


dotenv.read_dotenv()

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chilliboom.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
