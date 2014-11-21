#-*- coding:utf-8 -*-
"""
Eshop cotext processors

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""
from .models import Cart, ArticleCategory, ArticleItem
from django.core.cache import cache

def eshop(request):
    """ add current cart in template context """
    extra_context = {}
    extra_context['root_categories'] = ArticleCategory.objects.\
                    filter(parent=204, published=True)
    extra_context['brand_categories'] = ArticleCategory.objects.\
                    filter(parent=205, published=True)
    extra_context['slider_action'] = ArticleItem.objects.\
                    filter(action_product=True).order_by("order")
    extra_context['slider_new'] = ArticleItem.objects.\
                    filter(new_product=True).order_by("order")
    cart_id = request.session.get('cart', None)
    if cart_id is not None:
        cart_cache_name = u"cart_%d" % cart_id
        cart_obj = cache.get(cart_cache_name, None)
        if cart_obj is None:
            try:
                cart_obj = Cart.objects.get(pk=cart_id)
            except Cart.DoesNotExist:
                return {}
            cache.set(cart_cache_name, cart_obj)
            extra_context['cart'] = cart_obj
    return extra_context

