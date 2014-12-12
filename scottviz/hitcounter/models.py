from datetime import timedelta, datetime
from django.db import models
from django.utils.translation import ugettext as _
import settings

class Hit(models.Model):
    """
    hit model
    """
    time = models.DateTimeField(auto_now_add=True, editable=False)
    ipAddress = models.IPAddressField()
    session = models.CharField(max_length=40, null=True)
    url = models.CharField(_('URL'), max_length=2000)

    def save(self, *args, **kwargs):
        print self.ipAddress
        # save only if the required amount of time has passed since last visit
        if self.id:
            hits = Hit.objects.filter(ipAddress=self.ipAddress)
            hits = hits.filter(url=self.url)
            hits = hits.filter(session=self.session)
            hits = hits.filter(time__gt=self.time - timedelta(minutes=int(settings.TIME_BETWEEN_HITS)))

            if len(hits) == 0:
                super(Hit, self).save(*args, **kwargs)
        else:
            super(Hit, self).save(*args, **kwargs)

    def check_expiration(self):
        now = datetime.now()

        if self.time - timedelta(minutes=int(settings.HIT_EXPIRATION)) < now:
            self.delete()



