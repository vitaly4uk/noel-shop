from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.views.generic.list_detail import object_detail
from eshop.models import ArticleItem, ArticleCategorySitemap, ArticleItemSitemap
from main.models import News
from main.views import cached_sitemap, search_view, send_feedback, send_cart
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^admin/', include(admin.site.urls)),
    #(r'^robots.txt$', include('robots.urls')),
    (r'^sitemap\.xml$', cached_sitemap),
    (r'^captcha/', include('captcha.urls')),
    (r'^eshop/', include('eshop.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^search/$', search_view, {}, 'search'),
    url(r'^news/(?P<slug>[-\w]+)/$', object_detail, {
        'queryset' : News.objects.filter(published=True),
        'template_object_name' : 'news',
        },
        name='main_news_slug'),
    url(r'^send-feedback/$', send_feedback, name="send_feedback"),
    url(r'^send-cart/$', send_cart, name="send_cart"),
    (r'^$', direct_to_template, {
        'template': 'index.html',
        'extra_context': {
            'hot_sale': ArticleItem.objects.hot_sale(),
            },
        }),
    (r'^production/', direct_to_template, {
        'template':'production.html',
        }),
    (r'^news/', direct_to_template, {
        'template': 'news.html',
        'extra_context': {
            'all_news': News.objects.all_news(),
            },
        }),
    (r'^price/', direct_to_template, {
        'template': 'price.html',
        }),
    (r'^actions/', direct_to_template, {
        'template': 'actions.html',
        }),
    (r'^new/', direct_to_template, {
        'template': 'new.html',
        }),
    (r'^robots.txt$', direct_to_template, {
        'template': 'robots.txt',
        }),
)
