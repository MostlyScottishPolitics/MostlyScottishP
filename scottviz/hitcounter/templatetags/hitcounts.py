from django import template
from hitcounter.models import HitCount


register = template.Library()


@register.simple_tag(takes_context=True)
def pagehits(context):
    """
    pagehits for current page
    """
    try:
        request = context['request']
        hit = HitCount.objects.get(url=request.path)
        return hit.hits
    except HitCount.DoesNotExist:
        return 0


@register.simple_tag
def pagehits_url(path):
    """
   hits by url
    """
    try:
        hit = HitCount.objects.get(url=path)
        return hit.hits
    except HitCount.DoesNotExist:
        return 0
