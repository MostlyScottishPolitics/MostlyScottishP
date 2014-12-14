from django.core.management.base import NoArgsCommand
from django.db import transaction, DatabaseError

from populate import populate_basics, updatedb, populate_divisions

class Command(NoArgsCommand):

    help = 'Populate database'

    def handle_noargs(self, **options):
        try:
            populate_basics.main()
            updatedb.main()
            populate_divisions.main()

        except DatabaseError:
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                # Log or handle otherwise
                pass