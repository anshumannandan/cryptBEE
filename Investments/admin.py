from django.contrib import admin
from . models import *
from django.contrib.admin import ModelAdmin
from django.forms import Textarea


class CoinAdmin(ModelAdmin):
    list_display = ['Name', 'FullName', 'Price', 'ChangePct']


class PANAdmin(ModelAdmin):
    list_display = ['user', 'pan_number']


class WalletAdmin(ModelAdmin):
    list_display = ['user', 'amount']


class MyHoldingsAdmin(ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows':20, 'cols':20})},
    }
    list_display = ['user']


class TransactionHistoryAdmin(ModelAdmin):
    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows':20, 'cols':85})},
    }
    list_display = ['user']


admin.site.register(Coin, CoinAdmin)
admin.site.register(PAN_Verification, PANAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(MyHoldings, MyHoldingsAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)