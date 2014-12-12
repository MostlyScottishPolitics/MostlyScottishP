from django.contrib.contenttypes.models import ContentType
from django.db.models import F

__author__ = 'laura'
from models import HitCount


class HitCountMiddleware(object):
    def process_request(self, request, *args, **kwargs):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip_adds = request.META['HTTP_X_FORWARDED_FOR'].split(",")
            ip = ip_adds[0]
        else:
            ip = request.META['REMOTE_ADDR']
        session = request.session.session_key
        hit, hit_created = HitCount.objects.get_or_create(url=request.path, ipAddress=ip, session=session)
        hit.save()

        return None

