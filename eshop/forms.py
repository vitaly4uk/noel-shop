from django import forms
from eshop.models import ArticleItem, CartItem
from tagging.fields import TagField
from django.utils.translation import ugettext as _
from eshop.widgets import CartItemWidget

class ArticleItemAdminForm(forms.ModelForm):

    tags = TagField()

    class Meta:
        model = ArticleItem

class CartItemAdminForm(forms.ModelForm):

    item        = forms.IntegerField(label=_('article'), widget=CartItemWidget(CartItem._meta.get_field('item').rel))
    quantity    = forms.DecimalField(label=_('quantity'), widget=forms.TextInput(attrs={'size':'4'}))
    price       = forms.DecimalField(label=_('price'), widget=forms.TextInput(attrs={'size':'8'}))
    total_price = forms.DecimalField(label=_('total'), widget=forms.TextInput(attrs={'size':'4'}), required=False)

    class Meta:
        model = CartItem
