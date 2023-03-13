from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


#CREATE-TOKEN-WHEN-CREATE-USER

class AdminPanel(UserAdmin):
    list_display = ('username', 'email', 'phone', 'usage_limit', 'usage_count', 'token')

    def token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return "-"

    def phone(self, obj):
        return obj.phone if hasattr(obj, 'phone') and obj.phone is not None else "-"

    def usage_limit(self, obj):
        return 100

    def usage_count(self, obj):
        return obj.usage_rights if hasattr(obj, 'usage_rights') else "-"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            token = Token.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, AdminPanel)

