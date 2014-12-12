from django.conf import settings

# Set the minimum time between two hits in minutes
TIME_BETWEEN_HITS = getattr(settings, 'TIME_BETWEEN_HITS', 60)

# Set delete time for hits in minutes
HIT_EXPIRATION = getattr(settings, 'HIT_EXPIRATION', 5*24*60)