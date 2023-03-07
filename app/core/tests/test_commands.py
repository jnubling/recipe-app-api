"""
Test custom Django management commands
"""

from unittest.mock import patch
# mocks the behaviour of the database to simulate
# rather the db is responding or not
from psycopg2 import OperationalError as Psycopg2OpError
# one of the errors it might gets once trying to connect
# to the db once it gets ready
from django.core.management import call_command
# alows calling the command that is being tested by its actual name
from django.db.utils import OperationalError
# another exception that might get once trying to connect to the db
from django.test import SimpleTestCase
# the base test class to be used for basic tests


@patch('core.management.commands.wait_for_db.Command.check')
# command that is used to mock the behaviour of the database
# (providing the path of the command)
# .check is provided by the BaseCommand lib.
class CommandTests(SimpleTestCase):
    """test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for database if db is ready"""
        patched_check.return_value = True
        # just returns the value true when checking the test
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    # mocks the behaviour of sleep,
    # providing the command path to "patched_sleep"
    def wait_for_db_delay(self, patched_sleep, patched_check):
        """test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]
        # raises some exceptions instead of retuning values
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        # it counts if the mocked check test was called 6 times
        # (2 * psycopg2error + 3 * operationalerror)
        patched_check.assert_called_with(databases=['default'])
