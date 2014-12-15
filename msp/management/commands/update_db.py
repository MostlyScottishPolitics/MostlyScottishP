from django.core.management.base import NoArgsCommand
from django.db import transaction, DatabaseError

from populate import updatedb

class Command(NoArgsCommand):

    help = 'Populate database'

    def handle_noargs(self, **options):
        try:
            updatedb.main()

        except DatabaseError:
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                # Log or handle otherwise
                pass