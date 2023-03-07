"""
Django command to wait for database to be available
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
# error django throws when db is not ready
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """entrypoint for command"""
        self.stdout.write('Waiting for database...')
        # logs a message to the screen
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                # checks the database connectivity
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
