from django.contrib import admin

# AdminPanel libraries
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.cache import cache

#API request calculate libraries
from datetime import datetime, timedelta
from .models import UserUsage
from django.utils import timezone

#User information 
class AdminPanel(UserAdmin):
    list_display = ('username', 'email', 'telephone', 'usage_count' , 'usage_limit', 'token', 'is_staff', 'is_superuser')

    def telephone(self, obj):
        return obj.last_name

    def token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return "-"
    
    def usage_limit(self, obj):
        if obj.is_staff or obj.is_superuser:
            return 1000
        else:
            return 100
    
    def usage_count(self, obj):
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        usage = UserUsage.objects.filter(user=obj, created__gte=month_start).count()
        return usage
    
    def reset_usage_count(obj):
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        usage = UserUsage.objects.filter(user=obj, created__gte=month_start)
        usage.delete()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            token = Token.objects.get_or_create(user=obj)

admin.site.unregister(User)
admin.site.register(User, AdminPanel)



"""
Reset usage_count
user = User.objects.get(username='admin')
AdminPanel.reset_usage_count(user)
"""
