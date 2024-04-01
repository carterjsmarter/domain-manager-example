from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from requests import request
from domains.models import User, Account, Domain


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'account')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'account')}),
    )
    list_display = (
        "id",
        "email",
    )

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_id",
        "account_name",
        "owner",
        "status",
    )

class DomainAdmin(admin.ModelAdmin):
    list_display = (
        "domain_id",
        "domain_name",
        "status",
    )

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Domain, DomainAdmin)