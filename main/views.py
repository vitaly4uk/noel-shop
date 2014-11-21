#-*- coding:utf-8 -*-
"""
Common project views

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""

from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.generic.list_detail import object_list
from django.contrib.sitemaps import FlatPageSitemap
from django.core.mail import mail_managers
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

import os

from datetime import date, timedelta
from main.models import News
from eshop.models import (ArticleCategorySitemap, ArticleItemSitemap,
        ArticleItem, Cart)


def cached_sitemap(request):
    """ generate simap.xml onec a day and show saved version """
    sitemap_filename = os.path.join(settings.PROJECT_ROOT, 'sitemap.xml')
    if os.path.exists(sitemap_filename) and (date.fromtimestamp(os.path.getmtime(sitemap_filename)) - date.today()) < timedelta(days=1):
        with open(sitemap_filename, "r") as sitemap_file:
            raw_data = HttpResponse(sitemap_file.read(), mimetype="text/xml")
    else:
        sitemaps = {
                'eshop_categories' : ArticleCategorySitemap,
                'eshop_items'      : ArticleItemSitemap,
                'flatpages'        : FlatPageSitemap,
                }
        raw_data = sitemap(request, sitemaps=sitemaps)
        with open(sitemap_filename, "w") as sitemap_file:
            sitemap_file.write(raw_data.content)
    return raw_data

def search_view(request):
    """ full-text articles search """
    lookup_text = unicode(request.GET.get('q', None))
    if lookup_text is None:
        query = ArticleItem.objects.none()
    else:
        query = ArticleItem.objects.filter(Q(name__icontains=lookup_text) | Q(kod_tovara__icontains=lookup_text))
    return object_list(request, queryset = query, template_name = "search.html", extra_context={'lookup_text':lookup_text})


def send_feedback(request):
    if request.method == "POST":
        message = u"Ф.И.О. - %s\ne-mail: %s\nТелефон: %s\n%s" % (request.POST.get('name'), request.POST.get('email'), request.POST.get('phone'), request.POST.get('message'))
        mail_managers("User feedback", message, fail_silently=False)
    return redirect('/')


def send_cart(request):
    if request.method == "POST":
        if request.session.get('cart', None):
            cart = get_object_or_404(Cart, pk=request.session.get('cart'))
        else:
            cart = Cart()
            if request.user.is_authenticated():
                cart.user  = request.user
                cart.email = request.user.email
                cart.name  = request.user.get_full_name()
            cart.save()
            request.session['cart'] = cart.pk

        if request.POST.get('submit') == u'Пересчитать':
            for item in cart:
                try:
                    new_quantity = int(request.POST.get(str(item.id), None))
                except ValueError:
                    continue
                if new_quantity is not None and item.quantity != new_quantity:
                    if new_quantity:
                        item.quantity = new_quantity
                        item.save()
                    else:
                        item.delete()

            return redirect('/eshop/cart')

        if request.POST.get('submit') == u'Оформить заказ':
            message = u"Ф.И.О. - %s\ne-mail: %s\nТелефон: %s\nАдрес: %s\nСпособ доставки: %s\nСпособ оплаты: %s\nПримечание: %s\n \n" % (request.POST.get('name'),
                    request.POST.get('email'),
                    request.POST.get('phone'),
                    request.POST.get('address'),
                    request.POST.get('delivery'),
                    request.POST.get('pay'),
                    request.POST.get('text', ''))
            for item in cart:
                message += u"%s, %s шт. (цена за шт. %s грн.) - Итого: %s грн.\n" % (item, item.quantity, item.price, item.get_total_price())
            message += u"\nОбщая сумма заказа: %s грн." % (cart.total_price())
            mail_managers("User cart", message, fail_silently=True)
    return redirect('/')
