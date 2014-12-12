from django.conf import settings

# Set the minimum time between two hits
TIME_BETWEEN_HITS = getattr(settings, 'TIME_BETWEEN_HITS', 60)
