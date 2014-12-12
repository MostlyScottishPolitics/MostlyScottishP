from datetime import timedelta, datetime
from django.core.management.base import NoArgsCommand
from hitcounter.models import Hit
from django.utils.timezone import now
from django.db import transaction, DatabaseError
from hitcounter import settings


class Command(NoArgsCommand):

    help = 'Expires event objects which are out-of-date'

    def handle_noargs(self, **options):
        try:
            print Hit.objects.filter(time__gt=datetime.now() - timedelta(minutes=int(settings.HIT_EXPIRATION))).delete()
        except DatabaseError:
            try:
                transaction.rollback()
            except transaction.TransactionManagementError:
                # Log or handle otherwise
                pass