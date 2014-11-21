"""
Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>

Description:
    Different custom template tags
"""
from django import template
from django.contrib.flatpages.models import FlatPage
from eshop.models import ArticleCategory

register = template.Library()

@register.inclusion_tag('eshop/root_categories.html')
def root_categories(selected_category=None):
    """ render root categories list """

    return {
            'root_categories'   : ArticleCategory.objects.filter(parent_id=True,
                published=True),
            'selected_category' : selected_category,
            }


@register.inclusion_tag("eshop/price_category_item.html")
def show_category_item(subcategory):
    """ render subcategories recursivly """

    return {'category': subcategory}
