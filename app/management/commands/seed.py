from django.core.management.base import BaseCommand
from app.models import Link

seed_links = [
    'https://www.basecampcodingacademy.org',
    'https://docs.djangoproject.com/en/2.0/',
    'https://github.com/BaseCampCoding/django-views',
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for link in seed_links:
            l = Link.shorten(link)
            print('Shortened:', link, '=>', l.short_code)
