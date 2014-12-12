from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from hitcounter import settings


class HitCount(models.Model):
    """
    hitcount model
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    ipAddress = models.IPAddressField()
    url = models.CharField(_('URL'), max_length=2000)
    hits = models.PositiveIntegerField(_('Hits'), default=0)

    def save(self, *args, **kwargs):
        print self.ipAddress
        if self.id:
            super(HitCount, self).save(*args, **kwargs)
        else:
            hits = HitCount.objects.filter(ipAddress=self.ipAddress)
            hits = hits.filter(url = self.url)
            if len(hits) == 0:
                super(HitCount, self).save(*args, **kwargs)


    class Meta:
        ordering = ('-created', '-modified')
        get_latest_by = 'created'