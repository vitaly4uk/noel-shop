#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.cache import cache
from django_extensions.db.fields import (CreationDateTimeField,
        ModificationDateTimeField, AutoSlugField)

class NewsManager(models.Manager):

    def all_news(self):
        return self.get_query_set().filter(published=True)

class Constant(models.Model):
    """ define application constants """

    name        = models.SlugField(_('name'))
    value       = models.TextField(_('value'))
    description = models.TextField(_('description'))
    site        = models.ForeignKey(Site, editable=False, default=settings.SITE_ID)

    @classmethod
    def get_const(cls, name, site=settings.SITE_ID):
        """ return const value """
        if not isinstance(site, int):
            site = site.pk
        cache_name = 'constant_%s_%d' % (name, site)
        value = cache.get(cache_name)
        if value is None:
            try:
                const = cls.objects.get(name=name, site__id=site)
            except cls.DoesNotExist:
                return None
            value = const.value
            cache.set(cache_name, value)
        return value

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        verbose_name = _('constant')
        verbose_name_plural = _('contants')
        unique_together = ('name', 'site')

class News(models.Model):
    """ Model for news."""

    name         = models.CharField(_('name'), max_length=255, unique=True)
    slug         = AutoSlugField(_('Slug'), populate_from='name', overwrite=True, editable=True)
    headline     = models.CharField(_('headline'), max_length=255)
    content      = models.TextField(_('content'))
    image        = models.URLField(_('image'), blank=True)
    published    = models.BooleanField(_('published'), default=True)
    created_date = CreationDateTimeField(_('creation date'))
    updated_date = ModificationDateTimeField(_('modification date'))

    objects = NewsManager()

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        """ return object url """
        if self.slug:
            return ('main_news_slug', (), {'slug' : self.slug})
        else:
            return ('main_news', (), {'object_id' : self.pk})

    class Meta:
        verbose_name = _('news_page')
        verbose_name_plural = _('news_pages')
        ordering = ['created_date']
