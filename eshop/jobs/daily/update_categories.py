from django_extensions.management.jobs import DailyJob

from eshop.models import ArticleItem, ArticleCategory


class Job(DailyJob):

    def execute(self):
        for item in ArticleItem.objects.all():
            if item.old_category:
                item.categories = [ArticleCategory.objects.get(pk=item.old_category),]
                item.old_category = 0
                item.save()

            if item.brand:
                try:
                    item.categories.add(ArticleCategory.objects.get(name=item.brand.name.strip()))
                except ArticleCategory.DoesNotExist:
                    print item.brand.name
                    continue
                else:
                    item.brand = None
                    item.save()
