from django.db import models
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


class Link(models.Model):
    original = models.URLField()

    @property
    def short_code(self):
        return self.id

    @staticmethod
    def shorten(url):
        '''Returns a newly created `Link` that shortens the provided url.
        If the url is invalid, `None` is returned.'''
        try:
            l = Link(original=url)
            l.full_clean()
            l.save()
            return l
        except ValidationError:
            return None

    @staticmethod
    def find_by_short_code(short_code):
        '''Tries to find a `Link` with the corresponding short code.

        If such a `Link` exists, it returns it.
        Otherwise, it returns `None`.
        '''
        try:
            return Link.objects.get(id=short_code)
        except (Link.DoesNotExist, ValueError):
            return None
