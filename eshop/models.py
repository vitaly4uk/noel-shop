# -*- coding:utf-8 -*-
"""
Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>

Description:
    ecomerce models
"""
import threading
import random

from django.db import models
from django.contrib.sitemaps import Sitemap
from django.utils.translation import ugettext as _
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField, AutoSlugField)
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum

from main.models import Constant
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

import tagging
from tagging.models import Tag


class ArticleItemManager(models.Manager):
    def hot_sale(self):
        return self.get_query_set().filter(main_page=True).order_by("order")

    def slider_new(self):
        return self.get_query_set().filter(new_product=True)

    def slider_action(self):
        return self.get_query_set().filter(action_product=True)

    def published(self):
        return self.get_query_set().filter(published=True)


class ArticleCategory(MPTTModel):
    """ Model for article's category."""

    order = models.PositiveIntegerField(_('order'), default=0, db_column='_order')
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', overwrite=True, editable=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    image = models.ImageField(_('image'), upload_to="upload", blank=True)
    description = models.TextField(_('description'), blank=True)
    video = models.CharField(_('youtube'), max_length=255, blank=True)
    published = models.BooleanField(_('published'), default=True)
    created_date = CreationDateTimeField(_('creation date'))
    updated_date = ModificationDateTimeField(_('modification date'))
    logo = models.URLField(_('logo'), blank=True)

    def get_children_articles(self):
        """ return queryset of published children articles """

        return self.articles.filter(published=True, present="+")

    def get_random_image(self):
        """ return random article image """
        try:
            return random.choice(self.articles.values_list('image', flat=True))
        except IndexError:
            return self.image

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        """ return object url """
        if self.slug:
            return ('eshop_category_slug', (), {'slug': self.slug})
        else:
            return ('eshop_category', (), {'object_id': self.pk})

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']


class ArticleItem(models.Model):
    """ Model for article """

    order = models.PositiveIntegerField(_('order'), default=0, db_column='_order')
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', overwrite=True, editable=True)
    categories = TreeManyToManyField(ArticleCategory, null=True, related_name='articles')
    kod_tovara = models.CharField(_('kod'), max_length=255)
    description = models.TextField(_('description'))
    video = models.CharField(_('youtube'), max_length=255, blank=True)
    image = models.ImageField(_('image'), upload_to="upload", blank=True)
    published = models.BooleanField(_('published'), default=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    created_date = CreationDateTimeField(_('creation date'))
    updated_date = ModificationDateTimeField(_('modification date'))
    present = models.BooleanField(_('present'), default=True)
    main_page = models.BooleanField(_('Hot sale'), default=False)
    new_product = models.BooleanField(_('Slider New'), default=False)
    action_product = models.BooleanField(_('Slider Action'), default=False)
    old_price = models.DecimalField(_('old price'), max_digits=10, decimal_places=2, blank=True)

    objects = ArticleItemManager()

    @property
    def main_category(self):
        try:
            return self.categories.all()[0]
        except IndexError:
            return None

    def get_price(self):
        """ calculate price """
        try:
            return float(self.price) * float(Constant.get_const('currency'))
        except TypeError:
            return float(self.price)

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    def get_image(self):
        """ return or self image if it exist or image of category """

        try:
            return self.image
        except Exception:
            return None

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        """ return object url """
        if self.slug:
            return ('eshop_item_slug', (), {'slug': self.slug})
        else:
            return ('eshop_item', (), {'object_id': self.pk})

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-present', 'price', 'order', 'name']


class ArticleImage(models.Model):
    """ article item image """
    article = models.ForeignKey('ArticleItem')
    image = models.ImageField(upload_to="upload")


CART_STATUS = (
    (1, _('created')),
    (2, _('not paid')),
    (3, _('paid')),
    (4, _('delivared')),
    (5, _('closed')),
)


class CartItem(models.Model):
    """ article item in cart """
    cart = models.ForeignKey('Cart')
    item = models.ForeignKey(ArticleItem)
    quantity = models.PositiveIntegerField(_('quantity'), default=0)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    def get_price(self):
        """ calculate price """
        try:
            return float(self.price) * float(Constant.get_const('currency'))
        except TypeError:
            return float(self.price)

    def get_total_price(self):
        """ return item total price """
        try:
            return float(self.price) * float(self.quantity) * float(Constant.get_const('currency'))
        except TypeError:
            return float(self.price) * float(self.quantity)

    def __unicode__(self):
        return unicode(self.item)

    class Meta:
        unique_together = ('cart', 'item')


class Cart(models.Model):
    """ customers orders """
    status = models.PositiveSmallIntegerField(_('status'), choices=CART_STATUS, default=1)
    user = models.ForeignKey(User, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True)
    name = models.CharField(_('name'), blank=True, max_length=127)
    comment = models.TextField(_('comment'), blank=True)
    created_date = CreationDateTimeField(_('creation date'))
    updated_date = ModificationDateTimeField(_('modification date'))

    def clear_cache(self):
        pass

    def add(self, item, quantity):
        """ add item to cart """
        cartitem, _created = CartItem.objects.get_or_create(cart=self, item=item, price=item.price)
        cartitem.quantity += quantity
        cartitem.save()
        self.clear_cache()

    def remove(self, item):
        """ remove item from cart """
        CartItem.objects.filter(cart=self, item=item).delete()
        self.clear_cache()

    def quantity(self):
        """ count total quantity of cart """
        try:
            quantity = CartItem.objects.filter(cart=self).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        except IndexError:
            quantity = 0
        if quantity:
            return int(quantity)
        else:
            return 0

    def price(self):
        """ count total cart price """
        total_price = sum(float(item.price) * float(item.quantity) for item in self)
        return total_price

    def total_price(self):
        """ count total cart price """
        total_price = sum(item.get_total_price() for item in self)
        return total_price

    def __unicode__(self):
        return u"%s - %d" % (_('cart'), self.pk)

    def __iter__(self):
        """ cart items iterator """
        cartitems = list(CartItem.objects.filter(cart=self))
        for item in cartitems:
            yield item

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ['-updated_date', '-created_date']


class ArticleCategorySitemap(Sitemap):
    """Sitemap for articles category."""

    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ArticleCategory.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_date


class ArticleItemSitemap(Sitemap):
    """Sitemap for articles."""

    changefreq = "daily"
    priority = 0.8

    def items(self):
        return ArticleItem.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_date


tagging.register(ArticleItem)
