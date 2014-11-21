from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

from eshop.views import (add_to_cart, show_cart, category_detail,
        item_show_thumb, cat_show_thumb)
from eshop.models import ArticleCategory, ArticleItem

urlpatterns = patterns('',
        url(r'^category/(?P<object_id>\d+)/$', object_detail, {
            'queryset' : ArticleCategory.objects.filter(published=True),
            'template_object_name' : 'category',
            },
            name='eshop_category'),
        url(r'^category/(?P<slug>[-\w]+)/$', category_detail, name='eshop_category_slug'),

        url(r'^item/(?P<object_id>\d+)/$', object_detail, {
            'queryset' : ArticleItem.objects.filter(published=True),
            'template_object_name' : 'item',
            },
            name='eshop_item'),
        url(r'^item/(?P<slug>[-\w]+)/$', object_detail, {
            'queryset' : ArticleItem.objects.filter(published=True),
            'template_object_name' : 'item',
            },
            name='eshop_item_slug'),
        url(r'^item/(?P<object_id>\d+)/addtocart/(?P<quantity>\d+)/',
            add_to_cart,
            name="add_to_cart"),
        url(r'cart/$', show_cart, name="eshop-showcart"),
        url(r'^item_thumb/(?P<article_id>\w+)/(?P<size>\d+)/$', item_show_thumb, name='eshop_show_item_thumb'),
        url(r'^cat_thumb/(?P<category_id>\w+)/(?P<size>\d+)/$', cat_show_thumb, name='eshop_show_cat_thumb'),
)
