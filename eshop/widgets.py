#-*- coding:utf-8 -*-
"""
Special widgets for application

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext as _

class CartItemWidget(forms.TextInput):
    """
    A Widget for displaying/adding/deleting cart items
    """

    def __init__(self, rel, attrs=None, using=None):
        if isinstance(attrs, dict):
            attrs.setdefault('size', 8)
            attrs.setdefault('readonly', 'readonly')
        else:
            attrs = {'size':8, 'readonly':'readonly'}
        self.rel = rel
        self.db = using
        super(CartItemWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        related_url = '../../../%s/%s/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower())
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript looks for this hook.
        output = [super(CartItemWidget, self).render(name, value, attrs)]
        if value is None:
            output.append(u'<a href="%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' % \
                (related_url, name))
            output.append(u'<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))
