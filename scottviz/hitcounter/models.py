from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from hitcounter import settings


class HitCount(models.Model):
    """
    hitcount model
    """
    time = models.DateTimeField(auto_now_add=True, editable=False)
    #modified = models.DateTimeField(auto_now=True, editable=False)
    ipAddress = models.IPAddressField()
    session = models.CharField(max_length=40, null=True)
    url = models.CharField(_('URL'), max_length=2000)
    hits = models.PositiveIntegerField(_('Hits'), default=0)

    def save(self, *args, **kwargs):
        print self.ipAddress
        if self.id:
            hits = HitCount.objects.filter(ipAddress=self.ipAddress)
            hits = hits.filter(url=self.url)
            hits = hits.filter(session=self.session)
            hits = hits.filter(time__gt=self.time-timedelta(minutes=int(settings.TIME_BETWEEN_HITS)))

            if len(hits) == 0:
                super(HitCount, self).save(*args, **kwargs)
        else:
            super(HitCount, self).save(*args, **kwargs)
