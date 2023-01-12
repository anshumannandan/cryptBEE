from django.contrib import admin
from . models import *
from django.contrib.admin import ModelAdmin


class CoinAdmin(ModelAdmin):
    list_display = ['Name', 'FullName', 'Price', 'ChangePct']


class PANAdmin(ModelAdmin):
    list_display = ['user', 'pan_number']


admin.site.register(Coin, CoinAdmin)
admin.site.register(PAN_Verification, PANAdmin)