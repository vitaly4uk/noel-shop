from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.flatpages.admin import FlatPageAdmin as DefaultFlatPageAdmin
from django.conf import settings
from main.models import Constant, News
from django.utils.translation import ugettext as _

admin.site.unregister(User)
admin.site.unregister(FlatPage)

class ConstantAdmin(admin.ModelAdmin):
    """Customize constants admin page"""

    list_display = ('name', 'value', 'description')

    def queryset(self, request):
        """show only current site constants"""
        queryset = super(ConstantAdmin, self).queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(site=Site.objects.get_current())

    def save_model(self, request, obj, form, change):
        """ pre save actions """
        obj.site_id = settings.SITE_ID
        obj.save()

class UserAdmin(DefaultUserAdmin):
    """Customize user admin form"""

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter  = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )

    def queryset(self, request):
        """ hide superuser from list for non superusers """
        query = super(UserAdmin, self).queryset(request)
        if request.user.is_superuser:
            return query
        return query.exclude(is_superuser=True)


    def get_readonly_fields(self, request, obj=None):
        """ only superuser can edit all fields """
        if request.user.is_superuser:
            return ()
        if obj is not None and obj.is_superuser:
            return ('username', 'password', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff', 'is_superuser',
                    'user_permissions', 'groups', 'last_login', 'date_joined')
        fields = ['is_superuser', 'user_permissions', 'last_login', 'date_joined']
        if not request.user == obj:
            fields += ['password', 'email']
        if not request.user.has_perm('permission.can_change'):
            fields += ['is_active', 'is_staff', 'groups']

        return fields

class FlatPageAdmin(DefaultFlatPageAdmin):
    """Customize flatpage admin page"""

    readonly_fields = ('sites',)

    def queryset(self, request):
        """ show flatpages only for current site """
        return super(FlatPageAdmin, self).queryset(request).filter(
                sites=Site.objects.get_current())

    def save_model(self, request, obj, form, change):
        """ pre save actions """
        obj.save()
        if obj.sites.count() == 0:
            obj.sites.add(Site.objects.get_current())
            obj.save()

    class Media:
        js = ('tiny_mce/tiny_mce.js', 'tiny_mce/init.js')

class NewsAdmin(admin.ModelAdmin):
    """Customize news admin page"""

    list_display = ('name', 'published', 'created_date')
    list_filter  = ('published',)
    ordering     = ('name', 'created_date', 'published')
    prepopulated_fields = {"slug": ("name",)}

    class Media:
        js = ('tiny_mce/tiny_mce.js', 'tiny_mce/init.js')

admin.site.register(User, UserAdmin)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Constant, ConstantAdmin)
admin.site.register(News, NewsAdmin)
