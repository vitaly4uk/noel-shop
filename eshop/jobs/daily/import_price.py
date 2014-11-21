"""
Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>

Description:
    Daily job for import price
"""
from django_extensions.management.jobs import DailyJob
from eshop.models import ArticleCategory, ArticleItem
from tagging.models import Tag, TaggedItem
import urllib2
import zipfile
import StringIO
import xlrd
import os
from django.conf import settings

class Job(DailyJob):

    def execute(self):

        ArticleCategory.objects.update(published=False)
        ArticleItem.objects.update(published=False)
        inteh_price = zipfile.ZipFile(StringIO.StringIO(
            urllib2.urlopen('http://www.inteh.ua/inteh_price_new.zip').read()), 'r')

        xl_file = xlrd.open_workbook(file_contents = inteh_price.read(inteh_price.namelist()[0]))
        sheet = xl_file.sheet_by_index(0)
        current_cat = None
        for row_number in xrange(7, sheet.nrows):
            row_data = sheet.row(row_number)
            if row_data[0].ctype == xlrd.XL_CELL_EMPTY:
                current_cat, _ = ArticleCategory.objects.get_or_create(name = row_data[1].value)
                current_cat.published = True
                try:
                    current_cat.save()
                except Exception:
                    continue
            elif current_cat:
                tag, _ = Tag.objects.get_or_create(name='inteh_%d' % row_data[0].value)
                try:
                    item = TaggedItem.objects.get_by_model(ArticleItem, tag)[0]
                except IndexError:
                    item = ArticleItem()
                item.name      = row_data[1].value
                item.price     = unicode(row_data[2].value)
                item.warranty  = row_data[5].value
                item.present   = unicode(row_data[6].value)
                item.category  = current_cat
                item.published = True
                try:
                    item.save()
                except Exception:
                    continue
                Tag.objects.update_tags(item, tag)
        try:
            os.remove(os.path.join(settings.PROJECT_ROOT, 'sitemap.xml'))
        except OSError:
            pass
