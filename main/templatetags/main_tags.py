"""
Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>

Description:
    Different custom template tags
"""
from django import template
from django.contrib.sites.models import Site
from django.contrib.flatepages.models import FlatPage

register = template.Library()

@register.inclusion_tag('main/flatpage_links.html')
def flatpage_link():
    """ render flatpages links list """
    pages = FlatPage.objects.filter(sites=Site.get_current())
    return {
            'flatpage_links' : pages,
            }
