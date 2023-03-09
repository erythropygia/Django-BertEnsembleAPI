from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


#CREATE-TOKEN-WHEN-CREATE-USER

class UserAdminWithToken(UserAdmin):
    list_display = ('username', 'email', 'phone', 'token')
    
    def token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return "-"
        
    def phone(self, obj):
        return obj.phone.get(user=obj) if hasattr(obj, 'phone') else "-"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            token = Token.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, UserAdminWithToken)