#-*- coding:utf-8 -*-
"""
Eshop views

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""
import os
from PIL import Image

from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.utils import simplejson as json
from django.conf import settings

from eshop.models import ArticleItem, ArticleCategory, Cart


@never_cache
def add_to_cart(request, object_id, quantity=0):
    """ add item in cart """
    try:
        object_id = int(object_id)
    except ValueError:
        object_id = 0
    item = get_object_or_404(ArticleItem, pk=object_id) if object_id else None
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
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 0
    if quantity:
        cart.add(item, quantity)
    else:
        cart.remove(item)
    if request.is_ajax():
        data = {
                'total_count': u"%s" % cart.quantity(),
                'total_price': u"%.1f" % cart.total_price(),
                }
        return HttpResponse(json.dumps(data), mimetype="application/json")
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@never_cache
def show_cart(request):
    """ show cart """
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
    if request.method == "POST" and cart is not None:
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
    cart.clear_cache()
    return direct_to_template(request, 'eshop/cart.html', extra_context = {'cart' : cart})


def category_detail(request, slug):
    category = get_object_or_404(ArticleCategory, slug=slug)
    extra_context = {
            'category': category,
            'child_categories': category.get_children().order_by('name'),
            'child_articles': category.articles.published().order_by('-present', request.POST.get('sort_by', 'price')),
            }
    if 'brand' in request.GET:
        extra_context['child_articles'] = extra_context['child_articles'].filter(categories=request.GET['brand'])
    return direct_to_template(request, 'eshop/articlecategory_detail.html', extra_context = extra_context)


def item_show_thumb(request, article_id, size):
    article = get_object_or_404(ArticleItem, pk=article_id)
    return _show_thumbnail(request, article, size)


def cat_show_thumb(request, category_id, size):
    article = get_object_or_404(ArticleCategory, pk=category_id)
    return _show_thumbnail(request, article, size)


def _show_thumbnail(request, article, size):
    response = HttpResponse(mimetype='image/jpeg')

    image_file_name = u'%s/%s' % (settings.MEDIA_ROOT, article.image)
    thumb_file_name = u'%s/%s/%s/%s' % (settings.MEDIA_ROOT, 'thumb', size, article.image)

    try:
        if os.path.getmtime(image_file_name) > os.path.getmtime(thumb_file_name):
            os.remove(thumb_file_name)
    except OSError:
        pass

    try:
        im = Image.open(thumb_file_name)
    except IOError:
        try:
            im = Image.open(image_file_name)
            im.thumbnail((int(size), int(size)), Image.ANTIALIAS)
        except IOError:
            return response
        if im.format == "GIF":
            im = im.convert("RGB")
        im.save(thumb_file_name, "PNG")

    im.save(response, "PNG")
    return response
