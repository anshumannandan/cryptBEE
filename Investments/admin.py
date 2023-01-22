from django.contrib import admin
from . models import *
from django.contrib.admin import ModelAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_better_admin_arrayfield.forms.widgets import DynamicArrayTextareaWidget


class CoinAdmin(ModelAdmin):
    list_display = ['Name', 'FullName', 'Price', 'ChangePct']


class MyHoldingsAdmin(ModelAdmin, DynamicArrayMixin):
    formfield_overrides = {
        ArrayField: {'widget': DynamicArrayTextareaWidget(attrs={'rows':1, 'cols':70})},
    }
    list_display = ['user']


class TransactionHistoryAdmin(ModelAdmin, DynamicArrayMixin):
    formfield_overrides = {
        ArrayField: {'widget': DynamicArrayTextareaWidget(attrs={'rows':1, 'cols':90})},
    }
    list_display = ['user']


class MyWatchlistAdmin(ModelAdmin, DynamicArrayMixin):
    formfield_overrides = {
        ArrayField: {'widget': DynamicArrayTextareaWidget(attrs={'rows':1, 'cols':10})},
    }
    list_display = ['user']


class NewsAdmin(ModelAdmin):
    list_display = ['headline']


class BuyAdmin(ModelAdmin):
    list_display = ['user', 'coin', 'price']


class SellAdmin(ModelAdmin):
    list_display = ['user', 'coin', 'price']


admin.site.register(Coin, CoinAdmin)
admin.site.register(MyHoldings, MyHoldingsAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
admin.site.register(MyWatchlist, MyWatchlistAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(BuyLock, BuyAdmin)
admin.site.register(SellLock, SellAdmin)