from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ['id', 'name']
    list_display = ('id', 'name', 'email')
    list_filter = ('is_superuser',)
    filter_horizontal = ()
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )
    add_fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Two_Factor_Verification)
admin.site.register(Two_Factor_OTP)
admin.site.register(Email_OTP)
admin.site.register(PAN_Verification)
