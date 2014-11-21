"""
Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>

Description:
    Import descriptions of CPU from yandex market
"""
from django_extensions.management.jobs import WeeklyJob
from eshop.models import ArticleCategory, ArticleItem
from tagging.models import Tag, TaggedItem
import urllib2
import Levenshtein
from BeautifulSoup import BeautifulSoup

class Job(WeeklyJob):
    """ load articles description from yandex market """

    def execute(self):

        yandex_market_url = 'http://market.yandex.ru/guru.xml?hid=91019&CMD=-RR=0,0,0,0-VIS=201E2-CAT_ID=651600-EXC=1-PG=10-BPOS='
        bpos = 0
        yandex_cpus_list = []

        while True:
            page = BeautifulSoup(urllib2.urlopen(yandex_market_url + str(bpos)).read())
            bpos += 10
            tmp_list = [(item['href'], item.contents[0]) for item in page.findAll('a')
                    if item.has_key('id') and item['id'].startswith('item-href')]
            yandex_cpus_list += tmp_list
            if not tmp_list:
                break

        for item in ArticleCategory.objects.get(pk=1).get_children_articles():
            print sorted([(Levenshtein.ratio(item.name, unicode(ya_item[1])), item.name, ya_item[1]) for ya_item in yandex_cpus_list],
                    key=lambda i: i[0], reverse=True)[:3]
            print ' '

